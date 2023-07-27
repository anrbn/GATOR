# gator/arg_parsers/privesc_parser.py

from argparse import ArgumentParser
from gator.services.red.privesc import privesc_function_deploy

def privesc_parser(parent_parser=None):
    parser = ArgumentParser(add_help=False, parents=[parent_parser] if parent_parser is not None else [])
    
    parser.add_argument('deploy', help='Deploy and escalate privileges of a function')
    parser.add_argument('--project-id', required=True, help='The project ID.')
    parser.add_argument('--function-name', default=None, help='The name of the cloud function.')
    parser.add_argument('--runtime', default='python39', help='The runtime of the cloud function.')
    parser.add_argument('--entry-point', default='entry_point', help='The entry point of the cloud function.')
    parser.add_argument('--region', default='us-central1', help='The region of the cloud function.')
    parser.add_argument('--source', default=None, help='The source of the cloud function.')
    parser.add_argument('--service-account', default=None, help='The service account for the cloud function.')
    
    parser.set_defaults(func=privesc_function_deploy)
    return parser
