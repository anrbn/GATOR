# gator/arg_parsers/auth_parser.py

from argparse import ArgumentParser
from gator.auth.auth import auth_list, auth_activate, activate_service_account, auth_delete

def auth_parser(parent_parser):
    auth_arg_parser = ArgumentParser(add_help=False, parents=[parent_parser])
    subparsers = auth_arg_parser.add_subparsers(dest="subcommand")

    # Parser for 'list' subcommand
    list_parser = subparsers.add_parser('list')
    list_parser.set_defaults(func=auth_list)

    # Parser for 'activate' subcommand
    activate_parser = subparsers.add_parser('activate')
    activate_parser.add_argument('index', type=int, help='Activate an authentication mechanism by index.')
    activate_parser.set_defaults(func=auth_activate)

    # Parser for 'delete' subcommand
    delete_parser = subparsers.add_parser('delete')
    delete_parser.add_argument('indices', help='Indices of authentication mechanisms to delete, comma-separated, or "all".')
    delete_parser.set_defaults(func=auth_delete)

    # Arguments for 'auth' command
    auth_arg_parser.add_argument('--access-token', help='Access tokens for the service account.')
    auth_arg_parser.add_argument('--key-file', help='The path to the service account key file.')

    # Setting 'activate_service_account' function as default for 'auth' command
    auth_arg_parser.set_defaults(func=activate_service_account)

    return auth_arg_parser
