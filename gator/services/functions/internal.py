from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from gator.auth.credentials import load_credentials

import gator.helpers.print_helper as ph

def check_env_vars(args):
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v2', credentials=creds)
    region = args.region if args.region else 'us-central1'

    if args.function_name:
        try:
            request = service.projects().locations().functions().get(
                name=f'projects/{args.project_id}/locations/{region}/functions/{args.function_name}'
            )
            function = request.execute()

            ph.green(f"\n[+] Checking environment variables of function {function['name'].split('/')[-1]} in project {args.project_id} ...\n")

            service_config = function.get('serviceConfig', {})
            env_vars = service_config.get('environmentVariables', {})

            if not env_vars:
                ph.yellow("[!] No environment variables set.")
            else:
                for var, value in env_vars.items():
                    print(f"{var}: {value}")
            print()

        except HttpError as err:
            if err.resp.status == 404:
                ph.red(f"\n[-] Function '{args.function_name}' not found.\n")
            else:
                raise
    else:
        request = service.projects().locations().functions().list(
            parent=f'projects/{args.project_id}/locations/-'
        )
        response = request.execute()
        functions = response.get('functions', [])

        if not functions:
            ph.yellow(("\n[!] No Cloud Functions found in this Project.\n"))
        else:
            ph.green(f"\n[+] Checking environment variables of all functions in project {args.project_id} ...\n")
            for function in functions:
                check_env_vars_for_function(function, args.project_id)

def check_env_vars_for_function(function, project_id):

    service_config = function.get('serviceConfig', {})
    env_vars = service_config.get('environmentVariables', {})

    if not env_vars:
        ph.yellow("[!] No environment variables set.")
    else:
        for var, value in env_vars.items():
            print(f"- Cloud Function: {function['name'].split('/')[-1]}")
            print(f"  {var}: {value}")
    print()
