import click

from gator.custom.custom_cli import CustomGroup, CustomCommand
# from modules.functions import list_functions, list_function_triggers, functions_list_permissions
from gator.modules.functions import functions_list_permissions, functions_list_triggers, functions_list_functions

@click.group(cls=CustomGroup)
def functions():
    """Cloud Functions Command Group.
    Operations related to cloud functions, such as listing functions, their triggers, and permissions.
    """
    pass

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the functions.')
@click.option('-v', '--verbose', is_flag=True, help='Verbose Output.')
@click.option('--json-output', is_flag=True, help='Output in JSON format.')
def list(project_id, verbose, json_output):
    """List all cloud functions.
    This command will list all the cloud functions associated with the specified Project ID.
    """
    functions_list_functions(project_id, verbose, json_output)

functions.add_command(list, name="list")

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the functions.')
@click.option('--function-name', help='The name of the function.')
def triggers(project_id, function_name):
    """List triggers of a cloud function.
    This command will list all triggers of a cloud function associated with the specified function name and Project ID.
    """
    functions_list_triggers(project_id, function_name)

functions.add_command(triggers, name="triggers")

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the functions.')
def permissions(project_id):
    """List permissions of a cloud function.
    This command will list all permissions of a cloud function associated with the specified function name and Project ID.
    """
    functions_list_permissions(project_id)

functions.add_command(permissions, name="permissions")
