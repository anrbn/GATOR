import click

from gator.custom.custom_cli import CustomGroup, CustomCommand
from gator.modules.storage.buckets import storage_list_buckets
from gator.modules.storage.permissions import storage_list_permissions

@click.group(cls=CustomGroup)
def storage():
    """Cloud Storage Command Group. 
    Manage all aspects of storage, including buckets, files, and more.
    """
    pass

@click.group(cls=CustomGroup)
def buckets():
    """Buckets Sub-Command Group.
    Operations related to storage buckets, such as listing, creating, and deleting buckets.
    """
    pass

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the buckets.')
@click.option('-v', '--verbose', is_flag=True, help='Verbose Output.')
@click.option('--json-output', is_flag=True, help='Output in JSON format.')
def list_buckets(project_id, verbose, json_output):
    """List all storage buckets.
    This command will list all the storage buckets associated with the specified Project ID.
    
    Example:\n
        - gator storage buckets list --project-id abcd-1234
    """
    storage_list_buckets(project_id, verbose, json_output)

buckets.add_command(list_buckets, name="list")

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the buckets.')
@click.option('--bucket-name', help='The name of a specific bucket. If not specified, permissions for all buckets in the project will be listed.')
def list_permissions(project_id, bucket_name):
    """List permissions for storage buckets.
    This command will list permissions for a specific bucket or all buckets within the specified Project ID, depending on the --bucket-name option.
    
    Examples:\n
        - gator storage buckets list_permissions --project-id abcd-1234\n
        - gator storage buckets list_permissions --project-id abcd-1234 --bucket-name mybucket
    """
    storage_list_permissions(project_id, bucket_name)

buckets.add_command(list_permissions, name="permissions")
storage.add_command(buckets)