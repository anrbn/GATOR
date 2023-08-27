import click

from gator.custom.custom_cli import CustomGroup, CustomCommand
#from gator.modules.compute import compute_list_instances, compute_firewall, compute_impersonate, compute_inject_startup_script, compute_add_ssh_key
from gator.modules.compute import compute_add_ssh_key

@click.group(cls=CustomGroup)
def compute():
    """Compute Engine Command Group.
    Manage all aspects of compute, including instances, firewall rules, and more.
    """
    pass

@click.group(cls=CustomGroup)
def instances():
    """Instances Sub-Command Group.
    Operations related to compute instances, such as listing, manipulating firewall rules, and more.
    """
    pass

@click.command(cls=CustomCommand)
@click.option('--project-id', required=True, help='The project ID associated with the instances.')
@click.option('--email', required=True, help='Email address to generate the SSH key for.')
@click.option('--instance-name', required=True, help='Name of the Instance where the SSH key will be added.')
@click.option('--zone', required=True, help='The zone in which the Instance is located.')
def add_ssh_key(email, project_id, instance_name, zone):
    """Add SSH key to compute instances."""
    compute_add_ssh_key(email, project_id, instance_name, zone)

instances.add_command(add_ssh_key, name="add-ssh-key")

# @click.command(cls=CustomCommand)
# @click.option('--project-id', required=True, help='The project ID associated with the instances.')
# def list(project_id):
#     """List all compute instances.
#     This command will list all the compute instances associated with the specified Project ID.
#     """
#     #compute_list_instances(project_id)

# instances.add_command(list, name="list")

# @click.command(cls=CustomCommand)
# @click.option('--project-id', required=True, help='The project ID associated with the instances.')
# def firewall(project_id):
#     """Manipulate compute instances firewall rules.
#     """
#     #compute_firewall(project_id)

# instances.add_command(firewall, name="firewall")

# @click.command(cls=CustomCommand)
# @click.option('--project-id', required=True, help='The project ID associated with the instances.')
# def impersonate(project_id):
#     """Impersonate compute instances."""
#     #compute_impersonate(project_id)

# instances.add_command(impersonate, name="impersonate")

# @click.command(cls=CustomCommand)
# @click.option('--project-id', required=True, help='The project ID associated with the instances.')
# def inject_startup_script(project_id):
#     """Inject startup script into compute instances."""
#     #compute_inject_startup_script(project_id)

# instances.add_command(inject_startup_script, name="inject-startup-script")

compute.add_command(instances)
