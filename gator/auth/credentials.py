# gator/auth/credentials.py

import os
import json
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

STATE_FILE = "state.json"

def load_credentials(args):
    """Loads credentials based on the activated state."""

    # Check if state file exists
    if not os.path.exists(STATE_FILE):
        raise Exception("State file does not exist. Please authenticate first.")

    # Load state
    with open(STATE_FILE, 'r') as f:
        state = json.load(f)

    # Check if there is an activated authentication mechanism
    activated = state.get("activated")
    if not activated:
        raise Exception("No activated authentication mechanism. Please activate an authentication mechanism.")

    # Load credentials based on activated authentication mechanism
    if activated in state.get("key_files", []):
        # Load Service Account credentials from key file
        creds = service_account.Credentials.from_service_account_file(activated)

    elif activated in state.get("access_tokens", []):
        # Load credentials from access token
        creds = Credentials(activated)
        
    else:
        raise Exception("Invalid state. The activated authentication mechanism is not found.")
        
    return creds





