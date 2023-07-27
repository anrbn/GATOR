# gator/auth/credentials.py

import google.auth
from google.auth import exceptions
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

def load_credentials(args):
    """
    Function to load credentials based on the input arguments.
    """
    creds = None

    try:
        if args.access_token:
            creds = Credentials(args.access_token)
        elif args.sa_json_file:
            creds = service_account.Credentials.from_service_account_file(args.sa_json_file)
        elif args.gcloud:
            creds, _ = google.auth.default()

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

    except exceptions.DefaultCredentialsError as e:
        print(f"Failed to load credentials: {e}")

    return creds




