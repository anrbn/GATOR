# gator/services/storage/objects.py

from google.cloud import storage
from gator.auth.credentials import load_credentials
import json

def list_objects(args):
    """Lists all storage objects in a given bucket for a given project."""
    creds = load_credentials(args)
    client = storage.Client(credentials=creds, project=args.project_id)

    # Assume that bucket name is provided in args
    bucket_name = args.bucket_name
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()

    # Convert each blob's properties to JSON and print
    for blob in blobs:
        print(json.dumps(blob._properties, indent=4))
