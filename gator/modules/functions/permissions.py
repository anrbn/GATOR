# modules/functions/permissions.py

from googleapiclient.discovery import build

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def functions_list_permissions(project_id):
    try:
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return        
        service = build('cloudfunctions', 'v2', credentials=creds)

        response = service.projects().locations().functions().list(
            parent=f'projects/{project_id}/locations/-'
        ).execute()
        
        functions = response.get('functions', [])
        if not functions:
            ph.print_info("No Cloud Functions found in this Project.\n")
        else: 
            print(f"\n(+) Checking Permissions for Cloud Functions in project {project_id}\n")

            for function in functions:

                function_name = function["name"].split("/")[-1]
                ph.green(f'Cloud Function: {function_name}')

                permissions_response = service.projects().locations().functions().testIamPermissions(
                    resource=function['name'],
                    body={'permissions': [
                        'cloudfunctions.functions.call',
                        'cloudfunctions.functions.invoke',
                        'cloudfunctions.functions.delete',
                        'cloudfunctions.functions.get',
                        'cloudfunctions.functions.update',
                        'cloudfunctions.functions.sourceCodeGet',
                        'cloudfunctions.functions.sourceCodeSet',
                        'cloudfunctions.functions.getIamPolicy',
                        'cloudfunctions.functions.setIamPolicy'
                    ]}
                ).execute()

                print('   - Permissions:')
                for permission in permissions_response.get('permissions', []):
                    print(f'      - {permission}')

                iam_policy = service.projects().locations().functions().getIamPolicy(resource=function['name']).execute()
                public = False
                invoker_emails = []
                for binding in iam_policy.get('bindings', []):
                    if binding.get('role') == 'roles/cloudfunctions.invoker':
                        for member in binding.get('members', []):
                            if 'allUsers' in member or 'allAuthenticatedUsers' in member:
                                public = True
                            elif 'user:' in member or 'serviceAccount:' in member:
                                email = member.split(':', 1)[1]
                                invoker_emails.append(email)

                print(f'   - Public Accessibility: {"Yes" if public else "No"}')
                if invoker_emails:
                    print('   - Invoker Emails:')
                    for email in invoker_emails:
                        print(f'      - {email}')
                
                if 'serviceConfig' in function:
                    service_account_email = function['serviceConfig'].get('serviceAccountEmail', 'Not Available, as function is in Deployment State!')
                    print(f'   - Service Account: {service_account_email}')
                else:
                    print('   - Service Account: Not Available, as function is in Deployment State!')
                
                print()
    except Exception as ex:
        ph.print_error("{}".format(ex))
        print()