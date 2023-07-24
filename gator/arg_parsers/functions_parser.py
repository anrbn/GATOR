from argparse import ArgumentParser

from gator.services.functions.functions import list_functions, deploy_function

def functions_parser(parent_parser):
    functions_parser = ArgumentParser(add_help=False, parents=[parent_parser])

    subparsers = functions_parser.add_subparsers()

    # parser for 'list' command
    list_functions_parser = subparsers.add_parser('list', parents=[parent_parser])
    list_functions_parser.add_argument('--project-id', required=True, help='The project ID.')
    list_functions_parser.set_defaults(func=list_functions)

    # parser for 'deploy' command
    deploy_functions_parser = subparsers.add_parser('deploy', parents=[parent_parser])
    deploy_functions_parser.add_argument('--project-id', required=True, help='The project ID.')
    deploy_functions_parser.add_argument('--region', required=True, help='The region to deploy the function in.')
    deploy_functions_parser.add_argument('--function-name', required=True, help='The name of the function to deploy.')
    deploy_functions_parser.add_argument('--entry-point', required=True, help='The name of the function to execute in your source code.')
    deploy_functions_parser.add_argument('--runtime', required=True, help='The runtime in which your function executes.')
    deploy_functions_parser.add_argument('--source', required=True, help='The Cloud Storage URL where your function source code resides.')
    deploy_functions_parser.set_defaults(func=deploy_function)

    return functions_parser
