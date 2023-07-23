import json
from googleapiclient.discovery import build
from gator.auth.credentials import load_credentials

def list_functions(args):

    # Load the credentials
    creds = load_credentials(args)

    # Build the service
    service = build('cloudfunctions', 'v2', credentials=creds)
    parent = f'projects/{args.project_id}/locations/-'
    request = service.projects().locations().functions().list(parent=parent)

    response = request.execute()
    functions = response.get('functions', [])

    if not functions:
        print("No Cloud Functions found in this Project.")
    else:
        for function in functions:
            print(f"Function:\n{json.dumps(function, indent=4)}\n")
