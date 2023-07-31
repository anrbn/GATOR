# gator/arg_parsers/__init__.py

from argparse import ArgumentParser
from .iam_parser import iam_parser
from .storage_parser import storage_parser
from .functions_parser import functions_parser
from .privesc_parser import privesc_parser
from .auth_parser import auth_parser

def parse_args():
    parent_parser = ArgumentParser(add_help=False)

    parser = ArgumentParser(description='gator: A gcloud clone for managing Google Cloud resources.')
    subparsers = parser.add_subparsers(dest="command_group", help='Commands groups')

    subparsers.add_parser('iam', parents=[iam_parser(parent_parser)])
    subparsers.add_parser('auth', parents=[auth_parser(parent_parser)])
    subparsers.add_parser('storage', parents=[storage_parser(parent_parser)])
    subparsers.add_parser('functions', parents=[functions_parser(parent_parser)])
    subparsers.add_parser('privesc', parents=[privesc_parser(parent_parser)])

    args = parser.parse_args()

    return args

