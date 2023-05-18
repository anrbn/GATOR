"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        recon cloudsql-list
Description:    Lists Cloud SQL Instances available in the project with details.
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
        
        client = build('sqladmin', 'v1beta4', credentials=creds)
        instances = client.instances().list(project=project_id).execute()

        if not instances.get('items', None):
            output = f'{GREEN}+ No Cloud SQL Instances found in this Project.{RESET}'
        else:
            for instance in instances['items']:
                output += (f"{GREEN}+ Name:             {instance.get('name', 'N/A')}{RESET}\n")
                output += (f"  Instance type:    {instance.get('instanceType', 'N/A')}\n")
                output += (f"  Region:           {instance.get('region', 'N/A')}\n")
                output += (f"  Database version: {instance.get('databaseVersion', 'N/A')}\n")
                output += (f"  Tier:             {instance.get('settings', {}).get('tier', 'N/A')}\n")
                output += (f"  IP address:       {instance.get('ipAddresses', [{}])[0].get('ipAddress', 'N/A')}\n")
                output += (f"\n")
    
    except Exception as e:
        output += f"{RED}- An error occurred: {str(e)}{RESET}"

    print(output)
