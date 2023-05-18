"""
Author:         Anirban Das
                github.com/anrbn
                linkedin.com/in/anrbnds

Command:        recon storage-tree
Description:    Lists Cloud Storage buckets and objects present in the project in a tree view format.
"""

import colorama, platform
from treelib import Tree

import google.auth
from google.oauth2 import service_account
import google.oauth2.credentials

from google.cloud import storage


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

        client = storage.Client(project=project_id, credentials=creds)

        buckets = client.list_buckets()
        for bucket in buckets:
            tree = Tree()
            bucket_node_id = bucket.name
            bucket_node_text = f'{GREEN}- {bucket.name}{RESET}'
            tree.create_node(bucket_node_text, bucket_node_id)

            for blob in bucket.list_blobs():
                object_parts = blob.name.split('/')

                parent_id = bucket_node_id
                path_so_far = bucket_node_id
                for part in object_parts:
                    path_so_far = f'{path_so_far}/{part}'
                    if not tree.get_node(path_so_far):
                        tree.create_node(part, path_so_far, parent=parent_id)
                    parent_id = path_so_far
            tree.show()

    except Exception as e:
        output += f"{RED}- An error occurred: {str(e)}{RESET}"

    print(output)
