# gator/arg_parsers/privesc_parser.py

from argparse import ArgumentParser
from gator.services.red.privesc import privesc_function_deploy

def privesc_parser(parent_parser=None):
    privesc_parser = ArgumentParser(add_help=False, parents=[parent_parser] if parent_parser is not None else [])

    # Adding 'function' as a subparser
    function_parser = privesc_parser.add_subparsers().add_parser('function', parents=[parent_parser])

    deploy_parser = function_parser.add_subparsers().add_parser('deploy', parents=[parent_parser])
    deploy_parser.add_argument('--project-id', required=True, help='The project ID.')
    deploy_parser.add_argument('--function-name', default=None, help='The name of the cloud function.')
    deploy_parser.add_argument('--runtime', default='python39', help='The runtime of the cloud function.')
    deploy_parser.add_argument('--entry-point', default='anirban', help='The entry point of the cloud function.')
    deploy_parser.add_argument('--region', default='us-central1', help='The region of the cloud function.')
    deploy_parser.add_argument('--source', default='gs://anirban/function.zip', help='The source of the cloud function.')
    deploy_parser.add_argument('--service-account', default=None, help='The service account for the cloud function.')
    deploy_parser.add_argument('--member', default='allUsers', help='The member to add to the policy.')
    deploy_parser.add_argument('--role', default='roles/cloudfunctions.invoker', help='The role to give to the member.')    

    deploy_parser.set_defaults(func=privesc_function_deploy)
    return privesc_parser
