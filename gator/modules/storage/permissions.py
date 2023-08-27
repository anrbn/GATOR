from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def storage_list_permissions(project_id, bucket_name):
    """
    List permissions for Google Cloud Storage buckets for a given project.
    """
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

        if bucket_name:
            try:
                buckets = [service.buckets().get(bucket=bucket_name).execute()]
            except HttpError as e:
                ph.print_error(f"HTTP Error occurred while getting bucket {bucket_name}: {e}")
                return
            except Exception as e:
                ph.print_error(f"Failed to get bucket {bucket_name}: {e}")
                return
        else:
            try:
                request = service.buckets().list(project=project_id)
                response = request.execute()
                buckets = response.get('items', [])
            except HttpError as e:
                ph.print_error(f"HTTP Error occurred while listing buckets: {e}")
                return
            except Exception as e:
                ph.print_error(f"Failed to list buckets: {e}")
                return

        if not buckets:
            ph.print_info("No buckets found in this Project.\n")
        else:
            print(f"\n(+) Listing Permissions for buckets in the project {project_id}\n")
            
            for bucket in buckets:

                ph.green(f"Bucket: {bucket['name']}")
                print(f"   - Location: {bucket['location']}")
                iamConfiguration = bucket.get('iamConfiguration', {})
                print("   - IAM Configuration")
                bucketPolicyOnly = iamConfiguration.get('bucketPolicyOnly', {})
                policyStatus = "Enabled" if bucketPolicyOnly.get('enabled', False) else "Disabled"
                print(f"       - Bucket Policy Only: {policyStatus}")
                uniformBucketLevelAccess = iamConfiguration.get('uniformBucketLevelAccess', {})
                accessStatus = "Enabled" if uniformBucketLevelAccess.get('enabled', False) else "Disabled"
                print(f"       - Uniform Bucket Level Access: {accessStatus}")
                print(f"       - Public Access Prevention: {iamConfiguration.get('publicAccessPrevention', 'Null')}")
                print()
                
    except Exception as ex:
        ph.print_error(f"An unexpected error occurred: {ex}")
        print()
