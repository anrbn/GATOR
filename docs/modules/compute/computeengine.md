
# Compute Command Group

## Overview

The `compute` command group provides a set of sub-commands to manage Google Cloud Compute Engine resources. This includes operations related to compute instances such as adding SSH keys, manipulating firewall rules, and more.

## Sub-Commands

### instances

This is a sub-command group under `compute` that focuses on operations related to compute instances.

#### add-ssh-key

This command allows you to add an SSH key to a specific compute instance.

**Options:**

-   `--project-id`: The project ID associated with the compute instances. (Required)
-   `--email`: The email address for which the SSH key will be generated. (Required)
-   `--instance-name`: The name of the instance where the SSH key will be added. (Required)
-   `--zone`: The zone in which the instance is located. (Required)

**Example:**

```bash
gator compute instances add-ssh-key --project-id "your_project_id" --email "your_email" --instance-name "your_instance_name" --zone "your_zone"
```

This command will add an SSH key for the email provided to the specified instance in the given project and zone.

## Usage Scenarios

### Adding an SSH Key to an Instance

If you want to add an SSH key to an instance named `my-instance` in the project `my-project` located in the zone `zone-a`, you would run:

```bash
gator compute instances add-ssh-key --project-id "my-project" --email "user@example.com" --instance-name "my-instance" --zone "zone-a"
```

This will generate an SSH key for `user@example.com` and add it to the `my-instance` compute instance in the `my-project` project located in the `zone-a` zone.
