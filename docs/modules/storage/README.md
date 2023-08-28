# Cloud Storage Command Group

## Overview

The `storage` command group provides a set of sub-commands to manage Google Cloud Storage resources. This includes operations related to storage buckets such as listing them and managing their permissions.

## Sub-Commands

### buckets

This is a sub-command group under `storage` that focuses on operations related to storage buckets.

#### list

This command lists all the storage buckets associated with a specified Project ID.

**Options:**

-   `--project-id` (Required): The project ID associated with the storage buckets.
-   `-v, --verbose` (Optional): Enables verbose output.
-   `--json-output` (Optional): Outputs the list in JSON format.

**Example:**

```bash
gator storage buckets list --project-id "your_project_id" --verbose --json-output
```

#### permissions

This command lists permissions for a specific bucket or all buckets within the specified Project ID.

**Options:**

-   `--project-id` (Required): The project ID associated with the storage buckets.
-   `--bucket-name` (Optional): The name of a specific bucket. If not specified, permissions for all buckets in the project will be listed.

**Example:**

```bash
# To list permissions for a specific bucket
gator storage buckets permissions --project-id "your_project_id" --bucket-name "your_bucket_name"

# To list permissions for all buckets
gator storage buckets permissions --project-id "your_project_id"
```

## Usage Scenarios

### Listing All Storage Buckets

To list all storage buckets in a project with ID `my-project`, you would run:

```bash
gator storage buckets list --project-id "my-project"
```
For verbose output and JSON format, you can use:

```bash
gator storage buckets list --project-id "my-project" --verbose --json-output
```

### Listing Permissions of a Specific Storage Bucket

To list all permissions of a storage bucket named `my-bucket` in the project `my-project`, you would run:

```bash
gator storage buckets permissions --project-id "my-project" --bucket-name "my-bucket"
```

### Listing Permissions of All Storage Buckets

To list all permissions of storage buckets in the project `my-project`, you would run:

```bash
gator storage buckets permissions --project-id "my-project"
```
