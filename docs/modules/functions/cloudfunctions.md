
# Cloud Functions Command Group

## Overview

The `functions` command group provides a set of sub-commands to manage Google Cloud Functions. This includes operations such as listing functions, their triggers, and permissions.

## Sub-Commands

### list

This command lists all the Cloud Functions associated with a specified Project ID.

**Options:**

-   `--project-id` (Required): The project ID associated with the Cloud Functions.
-   `-v, --verbose` (Optional): Enables verbose output.
-   `--json-output` (Optional): Outputs the list in JSON format.

**Example:**

```bash
gator functions list --project-id "your_project_id" --verbose --json-output
```

### triggers

This command lists all the triggers associated with a specified cloud function and Project ID.

**Options:**

-   `--project-id` (Required): The project ID associated with the Cloud Functions.
-   `--function-name` (Optional): The name of the cloud function whose triggers you want to list.

**Example:**

```bash
gator functions triggers --project-id "your_project_id" --function-name "your_function_name"
```

### permissions

This command lists all the permissions associated with Cloud Functions for a specified Project ID.

**Options:**

-   `--project-id` (Required): The project ID associated with the Cloud Functions.

**Example:**

```bash
gator functions permissions --project-id "your_project_id"
```

## Usage Scenarios

### Listing All Cloud Functions

To list all Cloud Functions in a project with ID `my-project`, you would run:

```bash
gator functions list --project-id "my-project"
```

For verbose output and JSON format, you can use:

```bash
gator functions list --project-id "my-project" --verbose --json-output
```

### Listing Triggers of a Specific Cloud Function

To list all triggers of a cloud function named `my-function` in the project `my-project`, you would run:

```bash
gator functions triggers --project-id "my-project" --function-name "my-function"
```

### Listing Permissions of Cloud Functions

To list all permissions of Cloud Functions in the project `my-project`, you would run:

```bash
gator functions permissions --project-id "my-project"
```
