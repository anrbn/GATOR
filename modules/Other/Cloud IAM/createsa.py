"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        other createsa
Description:    Creates a New Service Account with Role : "Editor". 
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


def run_module(project_id, serviceaccountpath, active_access_token, account, roleid=None, sadisplayname=None):
    output = ""
    try:
        account = account.split("@")[0]

        if sadisplayname is None or sadisplayname == "default":
            sadisplayname = "Service Account"

        if serviceaccountpath is not None:
            creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
        elif active_access_token is not None:
            creds = google.oauth2.credentials.Credentials(active_access_token)
        else:
            output = f"{RED}- No valid authentication method provided.{RESET}\n"
            return output

        iam_service = build('iam', 'v1', credentials=creds)
        resource_manager_service = build('cloudresourcemanager', 'v1', credentials=creds)

        create_service_account = {
            'accountId': account,
            'serviceAccount': {
                'displayName': sadisplayname
            }
        }

        response = iam_service.projects().serviceAccounts().create(
            name=f'projects/{project_id}',
            body=create_service_account
        ).execute()
        output = f"{GREEN}+ Service account {response['email']} created successfully.{RESET}\n"

        if roleid is None or roleid == "default":
            role_ids = ["roles/editor"]
        else:
            role_ids = roleid.split(', ')

        policy = resource_manager_service.projects().getIamPolicy(resource=project_id, body={}).execute()
        for role_id in role_ids:
            binding = {
                'role': role_id.strip(),
                'members': [f'serviceAccount:{response["email"]}']
            }
            policy['bindings'].append(binding)
        resource_manager_service.projects().setIamPolicy(resource=project_id, body={'policy': policy}).execute()
        output = f"{GREEN}+ Roles {', '.join(role_ids)} granted to service account {response['email']}.{RESET}\n"
        return output

    except Exception as e:
        output = f"{RED}-  An error occurred: {str(e)}{RESET}"
        return output

