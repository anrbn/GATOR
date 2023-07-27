# gator/arg_parsers/__init__.py

from argparse import ArgumentParser
from .iam_parser import iam_parser
from .storage_parser import storage_parser
from .functions_parser import functions_parser
from .privesc_parser import privesc_parser

def parse_args():
    parent_parser = ArgumentParser(add_help=False)
    parent_parser.add_argument('--gcloud', action='store_true', help='Use gcloud for authentication.', required=False)
    parent_parser.add_argument('--sa-json-file', help='Path to the service account json file for authentication.', required=False)
    parent_parser.add_argument('--access-token', help='The access token for authentication.', required=False)

    parser = ArgumentParser(description='gator: A gcloud clone for managing Google Cloud resources.')
    subparsers = parser.add_subparsers(dest="command_group", help='Commands groups')

    subparsers.add_parser('iam', parents=[iam_parser(parent_parser)])
    subparsers.add_parser('storage', parents=[storage_parser(parent_parser)])
    subparsers.add_parser('functions', parents=[functions_parser(parent_parser)])
    subparsers.add_parser('privesc', parents=[privesc_parser(parent_parser)])

    args = parser.parse_args()

    if not any([args.gcloud, args.sa_json_file, args.access_token]):
        parser.error("No authentication method provided. Please provide at least one of the following: --gcloud, --sa-json-file, or --access-token.")

    return args
