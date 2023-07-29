# gator/services/functions/functions.py

import uuid
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gator.auth.credentials import load_credentials
import gator.helpers.print_helper as ph

def list_functions(args):
    if args.verbose and args.json_output:
        ph.red(("[-] Error: --verbose or -v and --json-output can't be used at the same time."))
        return
    
    ph.green((f"\n[+] Enumerating Cloud Functions for project {args.project_id} ...\n"))
    
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v2', credentials=creds)
    parent = f'projects/{args.project_id}/locations/-'
    request = service.projects().locations().functions().list(parent=parent)

    response = request.execute()
    functions = response.get('functions', [])

    if not functions:
        ph.yellow(("[!] No Cloud Functions found in this Project."))
    else:
        for function in functions:
            if args.json_output:
                print(json.dumps(function, indent=4))
                print()
                continue
            
            if not args.verbose:
                ph.green((f"Cloud Function: {function['name'].split('/')[-1]}"))
                print((f"   - Status: {function['state']}"))
                print((f"   - Entry Point: {function['buildConfig']['entryPoint']}"))
                print((f"   - Runtime: {function['buildConfig']['runtime']}"))
                print((f"   - Region: {function['name'].split('/')[3]}"))
                serviceConfig = function['serviceConfig']
                print((f"   - Service Account Email: {serviceConfig['serviceAccountEmail']}")) 

            elif args.verbose:
                ph.green((f"Cloud Function: {function['name'].split('/')[-1]}"))
                print((f"   - Status: {function['state']}"))
                print((f"   - Entry Point: {function['buildConfig']['entryPoint']}"))
                print((f"   - Runtime: {function['buildConfig']['runtime']}"))
                print((f"   - Region: {function['name'].split('/')[3]}"))
                print((f"   - Update Time: {function['updateTime']}"))
                labels = function['labels']
                print(("   - Labels:"))
                for label in labels.keys():
                    print((f"     - {label}: {labels[label]}"))
                print((f"   - Environment: {function['environment']}"))
                print((f"   - URL: {function['url']}"))

                if 'dockerRegistry' in function['buildConfig']:
                    print((f"     - Docker Registry: {function['buildConfig']['dockerRegistry']}"))
                else:
                    print((f"     - Docker Registry: None"))
                
                serviceConfig = function['serviceConfig']
                print(("   - Service Config:"))
                print((f"     - Timeout: {serviceConfig['timeoutSeconds']} seconds"))
                print((f"     - Max Instances: {serviceConfig['maxInstanceCount']}"))
                print((f"     - Ingress Settings: {serviceConfig['ingressSettings']}"))
                print((f"     - URI: {serviceConfig['uri']}"))
                print((f"     - Service Account Email: {serviceConfig['serviceAccountEmail']}"))
                print((f"     - Available Memory: {serviceConfig['availableMemory']}"))
                print((f"     - Revision: {serviceConfig['revision']}"))
                print((f"     - Max Instance Request Concurrency: {serviceConfig['maxInstanceRequestConcurrency']}"))
                
                if 'securityLevel' in serviceConfig:
                    print((f"     - Security Level: {serviceConfig['securityLevel']}"))
                else:
                    print((f"     - Security Level: None"))
            print()


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
        ph.green(f"[+] Function {function_name} created successfully.")
        return function_name  # return the function name
    except HttpError as error:
        ph.red(f"[-] Error: {error}")
        return None

