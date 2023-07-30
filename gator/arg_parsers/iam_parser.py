# gator/arg_parsers/iam_parser.py

from argparse import ArgumentParser
from gator.services.iam.service_accounts import list_service_accounts, download_service_account
from gator.services.iam.iam import set_iam_policy

def iam_parser(parent_parser):
    iam_parser = ArgumentParser(add_help=False, parents=[parent_parser])
    
    # Single subparsers instance
    subparsers = iam_parser.add_subparsers()

    # 'service-accounts' parser
    service_accounts_parser = subparsers.add_parser('service-accounts', parents=[parent_parser])
    service_accounts_subparsers = service_accounts_parser.add_subparsers()

    # 'service-accounts list' parser
    list_service_accounts_parser = service_accounts_subparsers.add_parser('list', parents=[parent_parser])
    list_service_accounts_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_service_accounts_parser.set_defaults(func=list_service_accounts)

    # 'service-accounts download' parser
    download_service_account_parser = service_accounts_subparsers.add_parser('download', parents=[parent_parser])
    download_service_account_parser.add_argument('--project-id', required=True, help='The project ID.')
    download_service_account_parser.add_argument('--service-account', required=True, help='The service account(s) to download keys for, separated by comma.')
    download_service_account_parser.add_argument('--format', required=True, help='The format to download the service account in.')
    download_service_account_parser.set_defaults(func=download_service_account)

    # 'set-iam-policy' parser
    set_iam_policy_parser = subparsers.add_parser('set-iam-policy', parents=[parent_parser])
    set_iam_policy_parser.add_argument('--project-id', required=True, help='The project ID.')
    set_iam_policy_parser.add_argument('--function-name', required=True, help='The name of the function.')
    set_iam_policy_parser.add_argument('--region', required=True, help='The region of the function.')
    set_iam_policy_parser.add_argument('--member', required=True, help='The member to add to the policy.')
    set_iam_policy_parser.add_argument('--role', required=True, help='The role to give to the member.')
    set_iam_policy_parser.set_defaults(func=set_iam_policy)

    return iam_parser
