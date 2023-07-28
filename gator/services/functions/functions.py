# gator/services/functions/functions.py

import uuid
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gator.auth.credentials import load_credentials

def list_functions(args):

    creds = load_credentials(args)
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


def deploy_function(args):
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v1', credentials=creds)

    # Default to 'us-central1' region if not provided
    region = args.region if args.region else 'us-central1'

    # Generate a random function name if not provided
    function_name = args.function_name if args.function_name else 'func' + str(uuid.uuid4())[:6]
    
    location = f'projects/{args.project_id}/locations/{region}'
    parent = service.projects().locations()

    function_dict = {
        'name': f'{location}/functions/{function_name}',
        'entryPoint': args.entry_point,
        'runtime': args.runtime,
        'httpsTrigger': {},
        'availableMemoryMb': 256,
        'sourceArchiveUrl': args.source,
    }

    # If a service account is provided, add it to the function_dict
    if hasattr(args, 'service_account') and args.service_account:
        function_dict['serviceAccountEmail'] = args.service_account

    try:
        function_request = parent.functions().create(location=location, body=function_dict)
        response = function_request.execute()
        print(f"[+] Function {function_name} created successfully.")
        return function_name  # return the function name
    except HttpError as error:
        print(f"[-] Error: {error}")
        return None

