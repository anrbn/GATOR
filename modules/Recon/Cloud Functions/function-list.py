"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        recon function-list
Description:    Lists Cloud Functions available in the project with details.
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

        service = build('cloudfunctions', 'v1', credentials=creds)
        parent = f'projects/{project_id}/locations/-'
        request = service.projects().locations().functions().list(parent=parent)

        response = request.execute()
        functions = response.get('functions', [])

        if not functions:
            output = f'{GREEN}+ No Cloud Functions found in this Project.{RESET}'
        else:
            for function in functions:
                full_func = function['name']
                function_name = full_func.split('/')[-1]
                output += f"\n{GREEN}+ {function_name}{RESET}\n"
                output += f"  Name: {function['name']}\n"
                output += f"  Trigger Type: {'HTTP Trigger' if 'httpsTrigger' in function else 'Event Trigger'}\n"
                output += f"  URL: {function.get('httpsTrigger', {}).get('url', 'N/A')}\n"
                output += f"  Security Level: {function.get('httpsTrigger', {}).get('securityLevel', 'N/A')}\n"
                output += f"  Status: {function['status']}\n"
                output += f"  Entry Point: {function['entryPoint']}\n"
                output += f"  Timeout: {function['timeout']}\n"
                output += f"  Available Memory: {function['availableMemoryMb']} MB\n"
                output += f"  Service Account Email: {function['serviceAccountEmail']}\n"
                output += f"  Update Time: {function['updateTime']}\n"
                output += f"  Version ID: {function['versionId']}\n"
                output += f"  Deployment Tool: {function.get('labels', {}).get('deployment-tool', 'N/A')}\n"
                output += f"  Source Upload URL: {function.get('sourceUploadUrl', 'N/A')}\n"
                output += f"  Source Archive URL: {function.get('sourceArchiveUrl', 'N/A')}\n"
                output += "  Source Repo:\n"
                output += f"    URL: {function.get('sourceRepository', {}).get('url', 'N/A')}\n"
                output += f"    Deployed URL: {function.get('sourceRepository', {}).get('deployedUrl', 'N/A')}\n"
                output += f"  Runtime: {function['runtime']}\n"
                output += f"  Ingress Settings: {function.get('ingressSettings', 'N/A')}\n"
                output += f"  Build ID: {function.get('labels', {}).get('build_id', 'N/A')}\n"
                output += f"  Build Name: {function.get('labels', {}).get('build_name', 'N/A')}\n"
                output += f"  Docker Registry: {'CONTAINER_REGISTRY' if function.get('labels', {}).get('docker_registry') == '1' else 'ARTIFACT_REGISTRY'}\n"

    except Exception as e:
        output += f"{RED}- An error occurred: {str(e)}{RESET}"

    print(output)