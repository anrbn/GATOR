# gator/auth/auth.py

import os
import json
from google.auth import default
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

STATE_FILE = "state.json"

def get_auth_elements():
    state = {}
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    elements = []
    if "key_files" in state:
        for key_file in state["key_files"]:
            elements.append(("Service Account", key_file))
    if "access_tokens" in state:
        for access_token in state["access_tokens"]:
            elements.append(("Access Token", access_token))
    return elements, state

def auth_list(args):
    elements, state = get_auth_elements()
    if elements:
        for i, element in enumerate(elements, 1):
            # Compare just the values for activation
            suffix = " [ACTIVATED]" if element[1] == state.get("activated") else ""
            print(f"{i}. {element[0]}: {element[1]}{suffix}")
            print()
    else:
        print("No Authentication mechanism set.")
        print()

def auth_activate(args):
    elements, state = get_auth_elements()
    if args.index > 0 and args.index <= len(elements):
        # Store just the value of the activated element
        state["activated"] = elements[args.index - 1][1]
        with open(STATE_FILE, "w") as f:
            json.dump(state, f)
    else:
        print("Invalid index for activation.")

def activate_service_account(args):
    state = {}

    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            state = json.load(f)
    
    if args.key_file:
        if "key_files" not in state:
            state["key_files"] = []
        if args.key_file not in state["key_files"]:
            state["key_files"].append(args.key_file)

    if args.access_token:
        if "access_tokens" not in state:
            state["access_tokens"] = []
        if args.access_token not in state["access_tokens"]:
            state["access_tokens"].append(args.access_token)
    
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def auth_delete(args):
    elements, state = get_auth_elements()

    if "all" in args.indices:
        state["key_files"] = []
        state["access_tokens"] = []
        state["activated"] = None
        print("Deleted all authentication mechanisms.")
    else:
        indices = list(map(int, args.indices.split(',')))
        for index in sorted(indices, reverse=True):
            if index > 0 and index <= len(elements):
                mechanism, value = elements[index - 1]
                if mechanism == "Service Account":
                    state["key_files"].remove(value)
                else:
                    state["access_tokens"].remove(value)

                if state.get("activated") == value:
                    state["activated"] = None

                print(f"Deleted authentication mechanism {index}.")
            else:
                print(f"Invalid index for deletion: {index}")

    # Write the updated state back to the file
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
