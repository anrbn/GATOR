import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def storage_list_buckets(project_id, verbose, json_output):
    """
    List Google Cloud Storage buckets for a given project.
    """
    if verbose and json_output:
        ph.print_error("The flag --verbose / -v and --json-output can't be used at the same time.\n")
        return

    try:
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return

        try:
            service = build('storage', 'v1', credentials=creds)
        except Exception as e:
            ph.print_error(f"Failed to build the storage service: {e}")
            return

        try:
            request = service.buckets().list(project=project_id)
            response = request.execute()
        except HttpError as e:
            ph.print_error(f"HTTP Error occurred while listing buckets: {e}")
            return
        except Exception as e:
            ph.print_error(f"Failed to list buckets: {e}")
            return

        buckets = response.get('items', [])
        if not buckets:
            ph.print_info("\nNo buckets found in this Project.\n")
        else:
            print(f"\n(+) Listing Buckets for project {project_id}\n")

            for bucket in buckets:
                if json_output:
                    print(json.dumps(bucket, indent=4))
                    print()
                    continue

                if not verbose:
                    ph.green((f"Bucket: {bucket['name']}"))
                    print(f"   - Location: {bucket['location']}")
                    print(f"   - Time Created: {bucket.get('timeCreated', 'Null')}")
                    print(f"   - Storage Class: {bucket['storageClass']}")
                    print(f"   - Updated: {bucket['updated']}")

                    cors = bucket.get('cors', [{}])[0]
                    print("   - CORS:")
                    print("     - Allowed Origin: ")
                    for origin in cors.get('origin', ['Null']):
                        print(f"        {origin}")
                    print("     - Method: ")
                    for method in cors.get('method', ['Null']):
                        print(f"        {method}")
                    print("     - Response Header: ")
                    for header in cors.get('responseHeader', ['Null']):
                        print(f"        {header}")          
                    print()

                elif verbose:
                    ph.green((f"Bucket: {bucket['name']}"))
                    print(f"   - Self Link: {bucket.get('selfLink', 'Null')}")
                    print(f"   - Etag: {bucket.get('etag', 'Null')}")
                    print(f"   - ID: {bucket.get('id', 'Null')}")
                    print(f"   - Location: {bucket.get('location', 'Null')}")
                    print(f"   - Time Created: {bucket.get('timeCreated', 'Null')}")            
                    print(f"   - Storage Class: {bucket.get('storageClass', 'Null')}")
                    print(f"   - Updated: {bucket.get('updated', 'Null')}")
                    print(f"   - Metageneration: {bucket.get('metageneration', 'Null')}")
                    print(f"   - Project Number: {bucket.get('projectNumber', 'Null')}")
                    print(f"   - Versioning Enabled: {bucket.get('versioning', {}).get('enabled', 'Null')}")
                    print(f"   - Location Type: {bucket.get('locationType', 'Null')}")
                    print(f"   - Satisfies PZS: {bucket.get('satisfiesPZS', 'Null')}")

                    lifecycle = bucket.get('lifecycle', {}).get('rule', [{}])[0]
                    print("   - Lifecycle:")
                    print("     - Rule:")
                    print(f"       - Action:")
                    print(f"         - Type: {lifecycle.get('action', {}).get('type', 'Null')}")
                    print(f"         - Age: {lifecycle.get('condition', {}).get('age', 'Null')}")
                    print("       - Condition:")
                    print(f"         - isLive: {lifecycle.get('condition', {}).get('isLive', 'Null')}")
                    print(f"         - numNewerVersions: {lifecycle.get('condition', {}).get('numNewerVersions', 'Null')}")

                    cors = bucket.get('cors', [{}])[0]
                    print("   - CORS:")
                    print("     - Allowed Origin: ")
                    for origin in cors.get('origin', ['Null']):
                        print(f"        {origin}")
                    print("     - Method: ")
                    for method in cors.get('method', ['Null']):
                        print(f"        {method}")
                    print("     - Response Header: ")
                    for header in cors.get('responseHeader', ['Null']):
                        print(f"        {header}")   

                    print(f"   - Satisfies PZS: {bucket.get('satisfiesPZS', 'Null')}")
                    print()

    except Exception as ex:
        ph.print_error(f"An unexpected error occurred: {ex}")
        print()
