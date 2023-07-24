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
    location = f'projects/{args.project_id}/locations/{args.region}'
    parent = service.projects().locations()

    function_dict = {
        'name': f'{location}/functions/{args.function_name}',
        'entryPoint': args.entry_point,
        'runtime': args.runtime,
        'httpsTrigger': {},
        'availableMemoryMb': 256,  
        'sourceArchiveUrl': args.source,
    }

    try:
        function_request = parent.functions().create(location=location, body=function_dict)
        response = function_request.execute()
        print(f"Function {args.function_name} created successfully.")
    except HttpError as error:
        print(f"An error occurred: {error}")
