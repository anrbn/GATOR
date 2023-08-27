import sys
from pathlib import Path
from googleapiclient import discovery, errors

from gator.utils import print_helpers as ph
from gator.utils.ssh_key import generate_ssh_key
from gator.auth.credentials import load_credentials


def compute_add_ssh_key(email, project_id, instance_name, zone):
    """
    Add an SSH key to a Google Cloud Compute instance.
    """
    try:
        creds = load_credentials()
        if creds is None:
            # ph.print_error("Failed to load credentials. Exiting.")
            return
        compute = discovery.build("compute", "v1", credentials=creds)

        instance_details = get_instance_details(project_id, zone, instance_name, compute)
        if instance_details:
            oslogin_project_status = check_oslogin_project_level(project_id, compute)
            ph.print_info(f"OS Login is {oslogin_project_status} at Project Level.")            
            oslogin_instance_status = check_oslogin_instance_level(instance_details)
            ph.print_info(f"OS Login is {oslogin_instance_status} at Instance Level.")

            block_ssh_keys_status = is_block_project_ssh_keys_enabled(instance_details)
            ph.print_info(f"Project-wide SSH keys are {block_ssh_keys_status}.")

            instance_external_ip = None
            for interface in instance_details.get("networkInterfaces", []):
                for config in interface.get("accessConfigs", []):
                    if "natIP" in config:
                        instance_external_ip = config["natIP"]
                        break
                if instance_external_ip:
                    break
            handle_ssh_key_addition(
                oslogin_project_status,
                oslogin_instance_status,
                block_ssh_keys_status,
                email,
                instance_name,
                instance_external_ip,
                project_id,
                zone,
                compute,
                creds,
            )
    except Exception as e:
        ph.print_error(f"An error occurred: {e}")


def handle_ssh_key_addition(
    oslogin_project_status,
    oslogin_instance_status,
    block_ssh_keys_status,
    email,
    instance_name,
    instance_external_ip,
    project_id,
    zone,
    compute,
    creds,
):
    """
    Handle the addition of an SSH key based on various conditions.
    """    
    try:
        username = email.split("@")[0]
        comment = email
        new_priv_key = False

        private_key, public_key, key_dir_priv = generate_ssh_key(
            username, comment, new_priv_key
        )

        if public_key is None:
            print("Failed to generate public key.")
            return

        key_directory = Path(key_dir_priv).parent    

        # Check for OS Login at the Instance level
        if oslogin_instance_status == "Enabled":
            add_public_key_to_oslogin(email, public_key, creds, key_directory, instance_name, key_dir_priv, instance_external_ip)
            # print("OS Login!")
            return

        if oslogin_project_status == "Enabled" and (
            oslogin_instance_status in ["Enabled", "Not Set"]
        ):
            add_public_key_to_oslogin(email, public_key, creds, key_directory, instance_name, key_dir_priv, instance_external_ip)
            # print("OS Login!")
            return

        if block_ssh_keys_status == "OFF":
            # Add SSH Key to both Instance and Project
            add_ssh_key_to_instance(
                project_id, zone, instance_name, username, public_key, compute
            )
            add_ssh_key_to_project(project_id, username, public_key, compute)
            ph.print_success("Adding SSH public key to both Project and Instance Level.")
        else:
            # Add SSH Key only to Instance
            add_ssh_key_to_instance(
                project_id, zone, instance_name, username, public_key, compute
            )
            ph.print_success("Adding SSH public key to Instance Level.")

        ph.print_info(f'Private and Public Key has been saved in "{key_directory}", use it to access {instance_name}.')
        ph.print_info(f'Usage: ssh -i "{key_dir_priv}" {username}@{instance_external_ip}\n')

    except errors.HttpError as e:
        ph.print_error(f"Error adding SSH key to OS Login for user {email}: {e}")
    except Exception as e:
        ph.print_error(f"An unexpected error occurred: {e}")


def add_ssh_key_to_instance(project_id, zone, instance_name, username, public_key, compute):
    """
    Add an SSH key directly to a Google Cloud Compute instance.
    """    
    try:
        instance = compute.instances().get(project=project_id, zone=zone, instance=instance_name).execute()
        metadata = instance.get("metadata", {})
        ssh_keys = [item["value"] for item in metadata.get("items", []) if item["key"] == "ssh-keys"]
        ssh_keys.append(f"{username}:{public_key}")
        metadata["items"] = [{"key": "ssh-keys", "value": "\n".join(ssh_keys)}]
        compute.instances().setMetadata(project=project_id, zone=zone, instance=instance_name, body=metadata).execute()
    except errors.HttpError as e:
        ph.print_error(f"Error adding SSH key to instance: {e}")
    except Exception as e:
        ph.print_error(f"An unexpected error occurred: {e}")


def add_ssh_key_to_project(project_id, username, public_key, compute):
    """
    Add an SSH key to the project level in Google Cloud.
    """
    try:
        project = compute.projects().get(project=project_id).execute()
        metadata = project.get("commonInstanceMetadata", {})
        ssh_keys = [item["value"] for item in metadata.get("items", []) if item["key"] == "ssh-keys"]
        ssh_keys.append(f"{username}:{public_key}")
        metadata["items"] = [{"key": "ssh-keys", "value": "\n".join(ssh_keys)}]
        compute.projects().setCommonInstanceMetadata(project=project_id, body=metadata).execute()
    except errors.HttpError as e:
        ph.print_error(f"Error adding SSH key to project: {e}")
    except Exception as e:
        ph.print_error(f"An unexpected error occurred: {e}")


def get_instance_details(project_id, zone, instance_name, compute):
    """
    Retrieve details of a specific Google Cloud Compute instance.
    """
    try:
        instance = compute.instances().get(project=project_id, zone=zone, instance=instance_name).execute()
        return instance
    except errors.HttpError as e:
        if e.resp.status == 404:
            ph.print_info("No Instance found with the given name in the specified Project and Zone.")
            return None
        else:
            ph.print_error(f"Error getting instance details: {e}")
            return None
    except Exception as e:
        ph.print_error(f"An unexpected error occurred: {e}")
        return None


def check_oslogin_project_level(project_id, compute):
    """
    Check the status of OS Login at the project level in Google Cloud.
    """
    try:
        response = compute.projects().get(project=project_id).execute()
    except errors.HttpError as e:
        ph.print_error(f"Error fetching project details: {e}")
        sys.exit(1)

    metadata_items = response.get("commonInstanceMetadata", {}).get("items", [])
    oslogin_project = next((item for item in metadata_items if item["key"] == "enable-oslogin"), None)

    if oslogin_project:
        return "Enabled" if oslogin_project["value"].lower() == "true" else "Disabled"
    else:
        return "Not Set"


def check_oslogin_instance_level(instance_details):
    """
    Check the status of OS Login at the instance level in Google Cloud.
    """
    try:
        metadata_items = instance_details.get("metadata", {}).get("items", [])
    except AttributeError:
        ph.print_error("Invalid instance details provided.")
        return "Error"

    oslogin_instance = next((item for item in metadata_items if item["key"] == "enable-oslogin"), None)

    if oslogin_instance:
        return "Enabled" if oslogin_instance["value"].lower() == "true" else "Disabled"
    else:
        return "Not Set"


def is_block_project_ssh_keys_enabled(instance_details):
    """
    Check if project-wide SSH keys are blocked for a Google Cloud Compute instance.
    """
    try:
        metadata = instance_details.get("metadata", {})
    except AttributeError:
        ph.print_error("Invalid instance details provided.")
        return "Error"

    for item in metadata.get("items", []):
        if item["key"] == "block-project-ssh-keys":
            return "ON" if item["value"].lower() == "true" else "OFF"

    return "OFF"


def add_public_key_to_oslogin(email, public_key, creds, key_directory, instance_name, key_dir_priv, instance_external_ip):
    """
    Add a public SSH key to a user's OS Login profile in Google Cloud.
    """
    oslogin = discovery.build('oslogin', 'v1', credentials=creds)

    ssh_key_body = {
        "key": public_key
    }

    try:
        response = oslogin.users().importSshPublicKey(
            parent=f"users/{email}",
            body=ssh_key_body
        ).execute()

        posix_accounts = response.get('loginProfile', {}).get('posixAccounts', [])
        if posix_accounts:
            posix_username = posix_accounts[0].get('username')

        ph.print_success(f"SSH key added to OS Login for user {email}.")
        ph.print_info(f'Private and Public Key has been saved in "{key_directory}", use it to access {instance_name}.')
        ph.print_info(f'Usage: ssh -i "{key_dir_priv}" {posix_username}@{instance_external_ip}\n')
        
    except errors.HttpError as e:
        ph.print_error(f"Error adding SSH key to OS Login for user {email}: {e}")
