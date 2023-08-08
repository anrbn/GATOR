# auth/credentials.py

import os
import json
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from gator.utils import print_helpers as ph

HOME = os.path.expanduser("~")
STATE_DIR = os.path.join(HOME, '.gator')
STATE_FILE = os.path.join(STATE_DIR, 'state.json')

# Ensure the .gator directory exists.
if not os.path.exists(STATE_DIR):
    os.makedirs(STATE_DIR)

def load_credentials():
    """Loads credentials based on the activated state."""
    
    if not os.path.exists(STATE_FILE):
        ph.print_error("state.json file not found. Ensure you have authenticated before proceeding.\n")
        return None
    
    with open(STATE_FILE, 'r') as f:
        try:
            state = json.load(f)
        except json.JSONDecodeError:
            ph.print_error("state.json file is corrupted. Please re-authenticate.\n")
            return None

    activated = state.get("activated")
    if not activated:
        ph.print_error("No activated authentication method. Please ensure an authentication mechanism is set as active.\n")
        return None

    if activated in state.get("key_files", []):
        return service_account.Credentials.from_service_account_file(activated)
    elif activated in state.get("access_tokens", []):
        return Credentials(activated)
    else:
        ph.print_error("Invalid state. The activated authentication mechanism is not recognized.\n")
        return None
