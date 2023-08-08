# main.py

import click

from custom.custom_cli import CustomGroup

from auth import auth_commands
from cli.storage_cli import storage
from cli.functions_cli import functions

@click.group(cls=CustomGroup)
def main():
    """GATOR - GCP Attack Toolkit for Offensive Research, a tool designed to aid in 
    research and exploiting Google Cloud Environments. It offers a comprehensive 
    range of modules tailored to support users in various attack stages, spanning 
    from Reconnaissance to Impact."""
    pass

main.add_command(auth_commands.auth)
main.add_command(storage)
main.add_command(functions)

if __name__ == '__main__':
    main()




