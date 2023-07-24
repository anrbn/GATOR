from argparse import ArgumentParser

from gator.services.iam.service_accounts import list_service_accounts

def iam_parser(parent_parser):
    iam_parser = ArgumentParser(add_help=False, parents=[parent_parser])

    service_accounts_parser = iam_parser.add_subparsers().add_parser('service-accounts', parents=[parent_parser])
    list_service_accounts_parser = service_accounts_parser.add_subparsers().add_parser('list', parents=[parent_parser])

    list_service_accounts_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_service_accounts_parser.set_defaults(func=list_service_accounts)

    return iam_parser
