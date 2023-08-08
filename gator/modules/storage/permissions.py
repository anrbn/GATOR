# modules/storage/permissions.py

from googleapiclient.discovery import build

from gator.auth.credentials import load_credentials
from gator.utils import print_helpers as ph

def storage_list_permissions(project_id, bucket_name):
    try:
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return
        service = build('storage', 'v1', credentials=creds)
        
        if bucket_name:
            buckets = [service.buckets().get(bucket=bucket_name).execute()]
        else: 
            request = service.buckets().list(project=project_id)
            response = request.execute()
            buckets = response.get('items', [])

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
        ph.print_error("{}".format(ex))
        print()
