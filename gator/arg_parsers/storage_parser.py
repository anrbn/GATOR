from argparse import ArgumentParser

from gator.services.storage.buckets import list_buckets
from gator.services.storage.objects import list_objects  # New import

def storage_parser(parent_parser):
    storage_parser = ArgumentParser(add_help=False, parents=[parent_parser])

    # Single subparsers instance
    subparsers = storage_parser.add_subparsers()

    # 'buckets' parser
    buckets_parser = subparsers.add_parser('buckets', parents=[parent_parser])
    list_buckets_parser = buckets_parser.add_subparsers().add_parser('list', parents=[parent_parser])
    list_buckets_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_buckets_parser.set_defaults(func=list_buckets)

    # 'objects' parser
    objects_parser = subparsers.add_parser('objects', parents=[parent_parser])
    list_objects_parser = objects_parser.add_subparsers().add_parser('list', parents=[parent_parser])
    list_objects_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_objects_parser.add_argument('--bucket-name', required=True, help='The bucket name.')
    list_objects_parser.set_defaults(func=list_objects)

    return storage_parser
