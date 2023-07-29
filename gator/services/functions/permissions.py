# gator/services/functions/permissions.py

from googleapiclient.discovery import build

from gator.auth.credentials import load_credentials
import gator.helpers.print_helper as ph

def check_permissions(args):

    creds = load_credentials(args)
    service = build('cloudfunctions', 'v2', credentials=creds)

    response = service.projects().locations().functions().list(
        parent=f'projects/{args.project_id}/locations/-'
    ).execute()
    
    functions = response.get('functions', [])
    if not functions:
        ph.yellow("\n[!] No Cloud Functions found in this Project.\n")
    else: 
        ph.green(f"\n[+] Checking Permissions for Cloud Functions in project {args.project_id} ...\n")

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




