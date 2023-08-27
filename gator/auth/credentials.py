import os
import json
from typing import Optional
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account

from gator.utils import print_helpers as ph

HOME = os.path.expanduser("~")
STATE_DIR = os.path.join(HOME, '.gator')
STATE_FILE = os.path.join(STATE_DIR, 'state.json')
KEY_FILES = "key_files"
ACCESS_TOKENS = "access_tokens"
ACTIVATED = "activated"

if not os.path.exists(STATE_DIR):
    os.makedirs(STATE_DIR)

def load_credentials() -> Optional[Credentials]:
    """
    Loads credentials based on the activated state.
    
    Returns:
        Credentials object if successful, None otherwise.
    """
    
    if not os.path.exists(STATE_FILE):
        ph.print_error("state.json file not found. Ensure you have authenticated before proceeding.")
        return None
    
    try:
        with open(STATE_FILE, 'r') as f:
            state = json.load(f)
    except json.JSONDecodeError:
        ph.print_error("state.json file is corrupted. Please re-authenticate.")
        return None

    activated_method = state.get(ACTIVATED)
    if not activated_method:
        ph.print_error("No activated authentication method. Please ensure an authentication mechanism is set as active.")
        return None

    key_files = state.get(KEY_FILES, [])
    access_tokens = state.get(ACCESS_TOKENS, [])
    
    if activated_method in key_files:
        try:
            return service_account.Credentials.from_service_account_file(activated_method)
        except Exception as e:
            ph.print_error(f"Failed to load service account credentials: {str(e)}")
            return None
    elif activated_method in access_tokens:
        try:
            return Credentials(activated_method)
        except Exception as e:
            ph.print_error(f"Failed to load access token credentials: {str(e)}")
            return None
    else:
        ph.print_error("Invalid state. The activated authentication mechanism is not recognized.")
        return None
