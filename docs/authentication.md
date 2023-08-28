# Authentication Command Group

## Overview

The `auth` command group provides a set of sub-commands that manages authentication. This includes operations related to add, list, activate, and delete authentication methods such as Service Accounts and Access Tokens. It let's you manage multiple authentication methods and easily switching between them.

## Authentication Methods

**gator** supports two types of authentication methods:

1. **Service Account:** A service account is a special type of Google account that belongs to your application instead of an individual end user. A key file associated with the service account is used for authentication.
2. **Access Token:** An access token is a string representing the granted permissions. It is used for authentication and authorization in the application.

## Sub-Commands

#### list

Lists all the authentication methods that have been added. It shows the type of authentication (Service Account or Access Token), the value (key file path or access token), and indicates which method is currently activated.

**Example:**

```bash
gator auth list
```

#### activate [INDEX]

Activates a specific authentication method based on its index. The index corresponds to the position of the authentication method in the list displayed by `gator auth list`.

**Example:**
```bash
gator auth activate 1
```

#### add

Adds either a key file or an access token to the list of authentication methods.

**Options:**

-   `--key-file` (Required): Path to the key file.
-   `--access-token` (Required): Access token for authentication.

**Examples:**
```bash
gator auth add --key-file "path/to/key_file.json"
```
```bash
gator auth add --access-token "your_access_token_here"
```

#### delete [INDICES]

Deletes a specific authentication method based on its index or removes all methods if 'all' is specified. The index corresponds to the position of the authentication method in the list displayed by `gator auth list`.

**Examples:**

```bash
gator auth delete 1
```

```bash
gator auth delete 1,2`
```

```bash
gator auth delete all
```

## Usage Scenarios

### Adding a New Service Account

To add a new service account, you need to provide the path to the key file associated with the service account.

```bash
gator auth add --key-file "path/to/key_file.json"
```

### Adding a New Access Token

To add a new access token, you need to provide the access token value.

```bash
gator auth add --access-token "your_access_token_here"
```

### Listing All Authentication Methods

To list all the added authentication methods and identify which one is currently activated, use the following command:

```bash
gator auth list
```

### Activating an Authentication Method

To activate a specific authentication method, you need to provide its index from the list of authentication methods.

```bash
gator auth activate 1
```

### Deleting an Authentication Method

To delete a specific authentication method, you need to provide its index from the list of authentication methods.

```bash
gator auth delete 1
gator auth delete 1, 5, 3
```

### Deleting All Authentication Methods

To delete all added authentication methods, use the following command:

```bash
gator auth delete all
```
