import click
import pkg_resources

from gator.custom.custom_cli import CustomGroup
from gator.auth import auth_commands
from gator.cli.storage_cli import storage
from gator.cli.functions_cli import functions
from gator.cli.compute_cli import compute

VERSION = pkg_resources.get_distribution("gator-red").version

@click.group(cls=CustomGroup)
@click.version_option(version=VERSION, prog_name="gator-red", message='%(version)s')
def main():
    """GATOR - GCP Attack Toolkit for Offensive Research, a tool designed to aid in 
    research and exploiting Google Cloud Environments. It offers a comprehensive 
    range of modules tailored to support users in various attack stages, spanning 
    from Reconnaissance to Impact."""
    pass

main.add_command(auth_commands.auth)
main.add_command(storage)
main.add_command(functions)
main.add_command(compute)

if __name__ == '__main__':
    main()
