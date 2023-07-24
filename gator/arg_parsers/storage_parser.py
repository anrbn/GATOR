from argparse import ArgumentParser

from gator.services.storage.buckets import list_buckets

def storage_parser(parent_parser):
    storage_parser = ArgumentParser(add_help=False, parents=[parent_parser])

    buckets_parser = storage_parser.add_subparsers().add_parser('buckets', parents=[parent_parser])
    list_buckets_parser = buckets_parser.add_subparsers().add_parser('list', parents=[parent_parser])

    list_buckets_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_buckets_parser.set_defaults(func=list_buckets)

    return storage_parser
