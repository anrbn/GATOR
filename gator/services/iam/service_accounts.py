# gator/services/iam/service_accounts.py

import json
from googleapiclient import discovery
from gator.auth.credentials import load_credentials

def list_service_accounts(args):
    """Lists all service accounts for a given project."""
    # Load the credentials
    creds = load_credentials(args)

    # Build the service
    service = discovery.build('iam', 'v1', credentials=creds)

    # Get the service accounts
    resource = f'projects/{args.project_id}'
    request = service.projects().serviceAccounts().list(name=resource)
    response = request.execute()

    # Print each service account in a pretty-printed JSON format
    #print(json.dumps(response['accounts'], indent=4))
    for account in response['accounts']:
        print(json.dumps(account, indent=4))