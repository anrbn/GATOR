"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        recon custom-roles
Description:    Lists all custom roles in the given project and their permissions.
"""

import colorama, platform

import google.auth
from google.oauth2 import service_account
import google.oauth2.credentials

from googleapiclient.discovery import build


if platform.system() == "Windows":
    colorama.init()

RESET = colorama.Style.RESET_ALL
BOLD = colorama.Style.BRIGHT
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA
BG_YELLOW = colorama.Back.YELLOW

def run_module(project_id, serviceaccountpath, active_access_token):
    output = ""
    try:
        if serviceaccountpath is not None:
            creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
        elif active_access_token is not None:
            creds = google.oauth2.credentials.Credentials(active_access_token)
        else:
            output = f"{RED}- No valid authentication method provided.{RESET}"
  
        service = build('iam', 'v1', credentials=creds)
        roles = service.projects().roles().list(parent=f'projects/{project_id}').execute().get('roles', [])
        if not roles:
            output += (f"{RED}- No roles found.{RESET}")
        for role in roles:
            output += (f"{GREEN}+   Role:          {role['title']}{RESET}\n")
            output += (f"    ID:            {role['name']}\n")
            output += (f"    Description:   {role['description']}\n")
            try:
                permissions = service.projects().roles().get(name=role['name']).execute().get('includedPermissions', [])
                if permissions:
                    output += (f"    Permissions:   {', '.join(permissions)}\n")
                else:
                    output += (f"    No permissions found for role {role['name']}\n")
                output += (f"\n")
                
            except Exception as e:
                output += f"\n{RED}  An error occurred: {str(e)}{RESET}\n"
            
    except Exception as e:
        output += f"{RED}- An error occurred: {str(e)}{RESET}"
        roles = []

    print(output)