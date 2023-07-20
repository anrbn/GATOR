import argparse
from gator.services.iam.service_accounts import list_service_accounts
from gator.services.storage.buckets import list_buckets

def parse_args():
    # Parent parser for shared arguments
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('--gcloud', action='store_true', help='Use gcloud for authentication.', required=False)
    parent_parser.add_argument('--service-account', help='Path to the service account json file for authentication.', required=False)
    parent_parser.add_argument('--access-token', help='The access token for authentication.', required=False)

    parser = argparse.ArgumentParser(description='gator: A gcloud clone for managing Google Cloud resources.', parents=[parent_parser])
    subparsers = parser.add_subparsers(dest="command_group", help='Commands groups')

    # IAM command group
    iam_parser = subparsers.add_parser('iam', help='Commands related to Identity and Access Management (IAM).', parents=[parent_parser])
    iam_subparsers = iam_parser.add_subparsers(dest='iam_command', help='IAM commands')

    # iam: list-service-accounts command
    list_service_accounts_parser = iam_subparsers.add_parser(
        'list-service-accounts',
        help='Lists all service accounts for a given project. Usage: iam list-service-accounts --project_id <project_id>',
        parents=[parent_parser]
    )
    list_service_accounts_parser.add_argument('--project_id', help='The project ID', required=True)
    list_service_accounts_parser.set_defaults(func=list_service_accounts)  # set function to call

    # Storage command group
    storage_parser = subparsers.add_parser('storage', help='Commands related to Google Cloud Storage.', parents=[parent_parser])
    storage_subparsers = storage_parser.add_subparsers(dest='storage_command', help='Storage commands')

    # storage: list-buckets command
    list_buckets_parser = storage_subparsers.add_parser(
        'list-buckets',
        help='Lists all storage buckets for a given project. Usage: storage list-buckets --project_id <project_id>',
        parents=[parent_parser]
    )
    list_buckets_parser.add_argument('--project_id', help='The project ID', required=True)
    list_buckets_parser.set_defaults(func=list_buckets)  # set function to call

    args = parser.parse_args()

    # Check if at least one authentication method is provided
    if not any([args.gcloud, args.service_account, args.access_token]):
        parser.error("No authentication method provided. Please provide at least one of the following: --gcloud, --service-account, or --access-token.")

    return args
