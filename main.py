# main.py

import click

from custom.custom_cli import CustomGroup

from cli import storage
from auth import auth_commands

@click.group(cls=CustomGroup)
def main():
    """GATOR - GCP Attack Toolkit for Offensive Research, a tool designed to aid in 
    research and exploiting Google Cloud Environments. It offers a comprehensive 
    range of modules tailored to support users in various attack stages, spanning 
    from Reconnaissance to Impact."""
    pass

main.add_command(storage)
main.add_command(auth_commands.auth)

if __name__ == '__main__':
    main()