from google.cloud import storage
from gator.auth.credentials import load_credentials

def list_buckets(args):
    """Lists all storage buckets for a given project."""
    creds = load_credentials(args)
    client = storage.Client(credentials=creds, project=args.project_id)
    buckets = client.list_buckets()

    # Return the buckets
    return [bucket.name for bucket in buckets]
