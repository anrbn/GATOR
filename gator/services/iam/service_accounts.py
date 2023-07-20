import json
from gator.auth.credentials import load_credentials
from googleapiclient import discovery

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

    # Return the service accounts in a pretty-printed JSON format
    return json.dumps(response['accounts'], indent=4)
