"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        other createroles
Description:    Creates custom roles in the project.
"""
import uuid, os
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


if os.path.exists("/.dockerenv"):
    permissions_txt_path = "/tmp/GATOR/dependent/permissions.txt"
#elif platform.system() == "Windows":
    #output_dir = "./download/Persistence/Cloud IAM/service-account-keys"
else:
    permissions_txt_path = "./dependent/permissions.txt"

if not os.path.isfile(permissions_txt_path):
    try:
        os.makedirs(os.path.dirname(permissions_txt_path), exist_ok=True)
        open(permissions_txt_path, 'x').close()
    except FileExistsError:
        pass


def run_module(project_id, serviceaccountpath, active_access_token, rolename=None, roleid=None, roledesc=None):
    output = ""
    try:
        if serviceaccountpath is not None:
            creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
        elif active_access_token is not None:
            creds = google.oauth2.credentials.Credentials(active_access_token)
        else:
            output = f"{RED}- No valid authentication method provided.{RESET}"
            return output

        service = build('iam', 'v1', credentials=creds)
        #permissions_txt_path = "./dependent/permissions.txt"
        with open(permissions_txt_path, 'r') as f:
            permissions = [line.strip() for line in f.readlines()]

        if roleid is None or roleid == 'default':
            roleid = str(uuid.uuid4()).replace('-', '')[:10]

        if rolename is None or rolename == 'default':
            rolename = uuid.uuid4().hex[:10]

        if roledesc is None or roledesc == 'default':
            roledesc = "Description"


        custom_role = {
            'roleId': roleid,
            'role': {
                'title': rolename,
                'description': roledesc,
                'includedPermissions': permissions
            }
        }

        service.projects().roles().create(parent=f'projects/{project_id}', body=custom_role).execute()


        output += (f'{GREEN}+ Custom role "{rolename}" created successfully.{RESET}')
        return output

    except Exception as e:
        output += f"{RED}  An error occurred: {str(e)}{RESET}"
        return output     