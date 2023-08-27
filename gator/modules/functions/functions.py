import uuid
import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def functions_list_functions(project_id, verbose, json_output):
    """
    List Google Cloud Functions for a given project.
    """
    try:
        if verbose and json_output:
            ph.print_error("--verbose or -v and --json-output can't be used at the same time.\n")
            return

        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return
        
        try:
            service = build('cloudfunctions', 'v2', credentials=creds)
            parent = f'projects/{project_id}/locations/-'
            request = service.projects().locations().functions().list(parent=parent)
            response = request.execute()
        except Exception as e:
            ph.print_error(f"Failed to list functions: {e}\n")
            return

        functions = response.get('functions', [])
        if not functions:
            ph.print_info("No Cloud Functions found in this Project.\n")
        else:
            print(f"\n(+) Listing Cloud Functions for Project {project_id}\n")
            for function in functions:
                if json_output:
                    print(json.dumps(function, indent=4))
                    print()
                    continue
                
                if not verbose:
                    ph.green(f"Cloud Function: {function['name'].split('/')[-1]}")
                    print(f"   - Status: {function['state']}")
                    print(f"   - Entry Point: {function['buildConfig']['entryPoint']}")
                    print(f"   - Runtime: {function['buildConfig']['runtime']}")
                    print(f"   - Region: {function['name'].split('/')[3]}")

                    """
                    if 'serviceConfig' in function:
                        serviceConfig = function['serviceConfig']
                        print(f"   - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}")
                    else:
                        print("   - Service Account Email: Null, as function is in Deployment State!")
                    """
                    serviceConfig = function.get('serviceConfig', {})
                    print(f"   - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}")
                    print()

                elif verbose:
                    ph.green(f"Cloud Function: {function['name'].split('/')[-1]}")
                    print(f"   - Status: {function.get('state', 'Null')}")
                    print(f"   - Entry Point: {function['buildConfig'].get('entryPoint', 'Null')}")
                    print(f"   - Runtime: {function['buildConfig'].get('runtime', 'Null')}")
                    print(f"   - Region: {function['name'].split('/')[3]}")
                    print(f"   - Update Time: {function.get('updateTime', 'Null')}")

                    labels = function.get('labels', {})
                    print("   - Labels:")
                    for label in labels.keys():
                        print(f"     - {label}: {labels[label]}")

                    print(f"   - Environment: {function.get('environment', 'Null')}")
                    print(f"   - URL: {function.get('url', 'Null')}")
                    print(f"   - Build: {function['buildConfig'].get('build', 'Null')}")

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

                    print(f"   - Docker Registry: {function['buildConfig'].get('dockerRegistry', 'None')}")

                    serviceConfig = function.get('serviceConfig', {})
                    print("   - Service Config:")
                    print(f"     - Service: {serviceConfig.get('service', 'Null')}")
                    print(f"     - Timeout: {serviceConfig.get('timeoutSeconds', 'Null')} seconds")
                    print(f"     - Max Instances: {serviceConfig.get('maxInstanceCount', 'Null')}")
                    print(f"     - Ingress Settings: {serviceConfig.get('ingressSettings', 'Null')}")
                    print(f"     - URI: {serviceConfig.get('uri', 'Null')}")
                    print(f"     - Service Account Email: {serviceConfig.get('serviceAccountEmail', 'Null, as function is in Deployment State!')}")
                    print(f"     - Available Memory: {serviceConfig.get('availableMemory', 'Null')}")
                    print(f"     - All Traffic On Latest Revision: {serviceConfig.get('allTrafficOnLatestRevision', 'Null')}")
                    print(f"     - Revision: {serviceConfig.get('revision', 'Null')}")
                    print(f"     - Max Instance Request Concurrency: {serviceConfig.get('maxInstanceRequestConcurrency', 'Null')}")
                    print(f"     - Available CPU: {serviceConfig.get('availableCpu', 'Null')}")
                    print(f"     - Security Level: {serviceConfig.get('securityLevel', 'None')}")
                    print()
    
    except Exception as ex:
        ph.print_error(f"An unexpected error occurred: {ex}")
        print()

def functions_deploy_functions(region, function_name, project_id, entry_point, runtime, service_account, source):
    """
    Deploy a Google Cloud Function.
    """
    try:
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return None

        try:
            service = build('cloudfunctions', 'v1', credentials=creds)
        except Exception as e:
            ph.print_error(f"Failed to build the cloudfunctions service: {e}\n")
            return None

        region = region if region else 'us-central1'
        function_name = function_name if function_name else 'func' + str(uuid.uuid4())[:6]
        location = f'projects/{project_id}/locations/{region}'
        parent = service.projects().locations()

        function_dict = {
            'name': f'{location}/functions/{function_name}',
            'entryPoint': entry_point,
            'runtime': runtime,
            'httpsTrigger': {},
            'availableMemoryMb': 256,
            'sourceArchiveUrl': source,
        }

        if service_account:
            function_dict['serviceAccountEmail'] = service_account

        try:
            function_request = parent.functions().create(location=location, body=function_dict)
            response = function_request.execute()
        except HttpError as error:
            ph.print_error(f"HTTP Error while creating function: {error}\n")
            return None
        except Exception as e:
            ph.print_error(f"Failed to create function: {e}\n")
            return None

        ph.print_success(f"Function {function_name} created successfully.")
        return function_name

    except Exception as ex:
        ph.print_error(f"An unexpected error occurred: {ex}\n")
        return None

    
