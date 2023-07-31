# gator/services/storage/buckets.py

from google.cloud import storage
from gator.auth.credentials import load_credentials
import json

def list_buckets(args):
    """Lists all storage buckets for a given project."""

    try:
        creds = load_credentials(args)
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    client = storage.Client(credentials=creds, project=args.project_id)
    buckets = client.list_buckets()

    for bucket in buckets:
        print(json.dumps(bucket._properties, indent=4))
