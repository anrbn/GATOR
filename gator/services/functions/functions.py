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
    
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v2', credentials=creds)
    parent = f'projects/{args.project_id}/locations/-'
    request = service.projects().locations().functions().list(parent=parent)

    response = request.execute()
    functions = response.get('functions', [])

    if not functions:
        ph.yellow(("\n[!] No Cloud Functions found in this Project.\n"))
    else:
        ph.green((f"\n[+] Enumerating Cloud Functions for project {args.project_id} ...\n"))
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

                """
                if 'serviceConfig' in function:
                    serviceConfig = function['serviceConfig']
                    print((f"   - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}"))
                else:
                    print("   - Service Account Email: Null, as function is in Deployment State!")
                """
                serviceConfig = function.get('serviceConfig', {})
                print((f"   - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}"))
                print()
            elif args.verbose:
                ph.green((f"Cloud Function: {function['name'].split('/')[-1]}"))
                print((f"   - Status: {function.get('state', 'Null')}"))
                print((f"   - Entry Point: {function['buildConfig'].get('entryPoint', 'Null')}"))
                print((f"   - Runtime: {function['buildConfig'].get('runtime', 'Null')}"))
                print((f"   - Region: {function['name'].split('/')[3]}"))
                print((f"   - Update Time: {function.get('updateTime', 'Null')}"))

                labels = function.get('labels', {})
                print("   - Labels:")
                for label in labels.keys():
                    print((f"     - {label}: {labels[label]}"))

                print((f"   - Environment: {function.get('environment', 'Null')}"))
                print((f"   - URL: {function.get('url', 'Null')}"))
                print((f"   - Build: {function['buildConfig'].get('build', 'Null')}"))

                source = function['buildConfig']['source'].get('storageSource', {})
                if source:
                    print("   - Source:")
                    for key, value in source.items():
                        print(f"     - {key}: {value}")
                else:
                    print("   - Source: Null")

                sourceProvenance = function['buildConfig'].get('sourceProvenance', {}).get('resolvedStorageSource', {})
                if sourceProvenance:
                    print("   - Source Provenance:")
                    for key, value in sourceProvenance.items():
                        print(f"     - {key}: {value}")
                else:
                    print("   - Source Provenance: Null")

                print((f"   - Docker Registry: {function['buildConfig'].get('dockerRegistry', 'None')}"))

                serviceConfig = function.get('serviceConfig', {})
                print("   - Service Config:")
                print((f"     - Service: {serviceConfig.get('service', 'Null')}"))
                print((f"     - Timeout: {serviceConfig.get('timeoutSeconds', 'Null')} seconds"))
                print((f"     - Max Instances: {serviceConfig.get('maxInstanceCount', 'Null')}"))
                print((f"     - Ingress Settings: {serviceConfig.get('ingressSettings', 'Null')}"))
                print((f"     - URI: {serviceConfig.get('uri', 'Null')}"))
                print((f"     - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}"))
                print((f"     - Available Memory: {serviceConfig.get('availableMemory', 'Null')}"))
                print((f"     - All Traffic On Latest Revision: {serviceConfig.get('allTrafficOnLatestRevision', 'Null')}"))
                print((f"     - Revision: {serviceConfig.get('revision', 'Null')}"))
                print((f"     - Max Instance Request Concurrency: {serviceConfig.get('maxInstanceRequestConcurrency', 'Null')}"))
                print((f"     - Available CPU: {serviceConfig.get('availableCpu', 'Null')}"))
                print((f"     - Security Level: {serviceConfig.get('securityLevel', 'None')}"))
                print()


def deploy_function(args):
    creds = load_credentials(args)
    service = build('cloudfunctions', 'v1', credentials=creds)

    region = args.region if args.region else 'us-central1'

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

    if hasattr(args, 'service_account') and args.service_account:
        function_dict['serviceAccountEmail'] = args.service_account

    try:
        function_request = parent.functions().create(location=location, body=function_dict)
        response = function_request.execute()
        ph.green(f"[+] Function {function_name} created successfully.")
        return function_name 
    except HttpError as error:
        ph.red(f"[-] Error: {error}")
        return None

# Work on Triggers

"""
{
    "name": "projects/coastal-height-389305/locations/us-central1/functions/function-5",
    "buildConfig": {
        "runtime": "nodejs20",
        "entryPoint": "helloAuditLog",
        "source": {
            "storageSource": {
                "bucket": "gcf-v2-sources-317420981291-us-central1",
                "object": "function-5/function-source.zip",
                "generation": "1690711904989774"
            }
        },
        "sourceProvenance": {}
    },
    "state": "DEPLOYING",
    "updateTime": "2023-07-30T10:12:06.150216726Z",
    "labels": {
        "deployment-tool": "console-cloud"
    },
    "stateMessages": [
        {
            "severity": "ERROR",
            "type": "CloudRunServiceNotFound",
            "message": "Cloud Run service projects/coastal-height-389305/locations/us-central1/services/function-5 for the function was not found. The function will not work correctly. Please redeploy."
        },
        {
            "severity": "ERROR",
            "type": "EventarcTriggerNotFound",
            "message": "Eventarc trigger projects/coastal-height-389305/locations/us-central1/triggers/function-5-759324 for the function was not found. The function may not work correctly. Please redeploy."
        }
    ],
    "environment": "GEN_2",
    "url": "https://us-central1-coastal-height-389305.cloudfunctions.net/function-5"
}
"""