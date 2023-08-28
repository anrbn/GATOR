# Documentation

-   [Installation](https://github.com/anrbn/GATOR/tree/main/docs#installation)
-   [Authentication](https://github.com/anrbn/GATOR/tree/main/docs#authentication)
-   [Modules](https://github.com/anrbn/GATOR/tree/main/docs#modules)
    -   [Compute Engine](https://github.com/anrbn/GATOR/tree/main/docs#1-compute-engine)
    -   [Cloud Functions](https://github.com/anrbn/GATOR/tree/main/docs#1-cloud-functions)
    -   [Cloud Storage](https://github.com/anrbn/GATOR/tree/main/docs#1-cloud-storage)
-   [Contributing](https://github.com/anrbn/GATOR/tree/main/docs#contributing)

## Installation

Python 3.11 or newer should be installed. You can verify your Python version with the following command:
```shell
python --version
```

### Manual Installation via setup.py

```shell
git clone https://github.com/anrbn/GATOR.git
cd GATOR
python setup.py install
```

### Automated Installation via pip

```shell
pip install gator-red
```

## Authentication

Gator provides a robust authentication management system. You can add, list, activate, and delete authentication methods such as Service Accounts and Access Tokens. For detailed instructions, see [Authentication Guide](https://github.com/anrbn/GATOR/blob/main/docs/authentication.md).

## Modules

### 1. Compute Engine
GATOR offers a comprehensive command set for managing Google Cloud Functions. You can list all cloud functions within a project, view the triggers associated with each function, and even inspect the permissions set on these functions. For detailed instructions, see [Compute Engine Guide](https://github.com/anrbn/GATOR/blob/main/docs/modules/compute/README.md).

### 2. Cloud Functions
GATOR offers a comprehensive command set for managing Cloud Storage. With Gator, you can list all storage buckets in a project and view their permissions. For detailed instructions, see [Cloud Functions Guide](https://github.com/anrbn/GATOR/blob/main/docs/modules/functions/README.md).

### 3. Cloud Storage
GATOR brings the power of Google Compute Engine management to your command line. For now it provides a single command to add SSH keys to instances. For detailed instructions, see [Cloud Storage Guide](https://github.com/anrbn/GATOR/blob/main/docs/modules/storage/README.md).

## Contributing

I warmly welcome and appreciate contributions from the community! If you're interested in contributing on any existing or new modules, feel free to submit a pull request (PR) with any new/existing modules or features you'd like to add.

Once you've submitted a PR, I'll review it as soon as I can. I might request some changes or improvements before merging your PR. Your contributions play a crucial role in making the tool better, and I'm excited to see what you'll bring to the project!

Thank you for considering contributing to the project!
