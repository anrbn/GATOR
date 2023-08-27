import os
import json
import click

from gator.utils import print_helpers as ph
from gator.custom.custom_cli import CustomGroup, CustomCommand

HOME = os.path.expanduser("~")
STATE_DIR = os.path.join(HOME, '.gator')
STATE_FILE = os.path.join(STATE_DIR, 'state.json')

if not os.path.exists(STATE_DIR):
    os.makedirs(STATE_DIR)

@click.group(cls=CustomGroup)
def auth():
    """Authentication Sub-Command Group.
    Commands related to authentication, including adding, listing, activating, and deleting authentication methods.
    """
    pass

def get_auth_elements():
    state = {}

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                # ph.print_error("State File is corrupted.")
                # ph.print_info("Fixing the state.json File.")
                # ph.print_info("Fixed!")
                # print()
                state = {}

    elements = []
    if "key_files" in state:
        for key_file in state["key_files"]:
            elements.append(("Service Account", key_file))
    if "access_tokens" in state:
        for access_token in state["access_tokens"]:
            elements.append(("Access Token", access_token))
    return elements, state
        
@click.command(cls=CustomCommand)
def auth_list():
    """List all authentication methods.

    This command lists all the authentication methods that have been added.

    Example:\n 
        - gator auth list
    """
    elements, state = get_auth_elements()
    if elements:
        header = "(+) Service Accounts / Access Tokens"
        separator = "-" * len(header)
        print()
        ph.yellow(f"{separator}\n{header}\n{separator}")
        print()
        
        for i, element in enumerate(elements, 1):
            if element[1] == state.get("activated"):
                suffix = " (ACTIVATED)"
                ph.green(f"{i}. {element[0]}: {element[1]}{suffix}")
            else:
                print(f"{i}. {element[0]}: {element[1]}")
            print()
            
        ph.yellow(separator)
        print()

    else:
        ph.print_error("No Authentication mechanism set.")
        print("          1. Import a Service Account / Access Token by using 'gator auth add --key-file <path to service_account> / --access-token <access_token>'")
        print("          2. Find the Index using 'gator auth list'")
        print("          3. Activate the Service Account / Access Token using 'gator auth activate (INDEX)'")
        print()
auth.add_command(auth_list, name="list")

@auth.command(name='activate', cls=CustomCommand)
@click.argument('index', type=int)
def auth_activate(index):
    """Activate a specific authentication method.

    Activates an authentication method based on its index.

    Example:\n
    - gator auth activate (INDEX)
    """
    elements, state = get_auth_elements()
    if index > 0 and index <= len(elements):
        state["activated"] = elements[index - 1][1]
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
        ph.print_success(f"Index {index} activated.\n")
    else:
        ph.print_error("Invalid index for activation.\n")

@auth.command(name='add', cls=CustomCommand)
@click.option('--key-file', default=None, help='Path to the key file.')
@click.option('--access-token', default=None, help='Access token for authentication.')
def activate_service_account(key_file, access_token):
    """Add an authentication method.

    Adds either a key file or an access token to the Index.

    Examples:\n
        - gator auth add --key-file "path/to/key_file"\n
        - gator auth add --access-token "access_token"
    """
    if not key_file and not access_token:
        ph.print_error("Either --key-file or --access-token should be provided.\n")
        return
    if key_file and access_token:
        ph.print_error("You can only provide one of --key-file or --access-token, not both.\n")
        return

    state = {}

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            try:
                state = json.load(f)
            except json.JSONDecodeError:
                # ph.print_error("State File is corrupted.")
                # ph.print_info("Fixing the state.json File.")
                # ph.print_info("Fixed!")
                # print()
                state = {}
    
    if key_file:
        if "key_files" not in state:
            state["key_files"] = []
        if key_file not in state["key_files"]:
            state["key_files"].append(key_file)
            ph.print_success(f"Key File '{key_file}' imported.")
        else:
            ph.print_info(f"Key File '{key_file}' already imported.")
        
    if access_token:
        if "access_tokens" not in state:
            state["access_tokens"] = []
        if access_token not in state["access_tokens"]:
            state["access_tokens"].append(access_token)
            ph.print_success("Access Token imported.")
        else:
            ph.print_info("Access Token already imported.")
    
    print()

    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

@auth.command(name='delete', cls=CustomCommand)
@click.argument('indices', type=str)
def auth_delete(indices):
    """Delete a specific authentication method.

    Deletes an authentication method based on its index or removes all 
    methods if 'all' is specified.

    Examples:\n                                                                
        - gator auth delete 1\n
        - gator auth delete 1,2\n
        - gator auth delete all
    """
    
    elements, state = get_auth_elements()
    
    if indices.lower() == "all":
        state["key_files"] = []
        state["access_tokens"] = []
        state["activated"] = None
        ph.print_success("Deleted all authentication mechanisms.\n")
    else:
        indices_list = [int(idx.strip()) for idx in indices.split(',')]
        
        for index in sorted(indices_list, reverse=True):
            if index > 0 and index <= len(elements):
                mechanism, value = elements[index - 1]
                if mechanism == "Service Account":
                    state["key_files"].remove(value)
                else:
                    state["access_tokens"].remove(value)
                
                if state.get("activated") == value:
                    state["activated"] = None

                ph.print_success(f"Deleted authentication mechanism {index}")
            else:
                ph.print_error(f"Invalid index for deletion: {index}")
        print()
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)