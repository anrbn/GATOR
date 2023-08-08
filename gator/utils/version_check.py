import requests
import os
import click

def get_installed_version():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    version_path = os.path.join(base_dir, "VERSION")
    
    with open(version_path, "r") as v:
        return v.read().strip()

def check_latest_version():
    current_version = get_installed_version()
    response = requests.get('https://pypi.org/pypi/gator-red/json')
    latest_version = response.json()['info']['version']

    if current_version != latest_version:
        click.echo(f"Update available! You're using gator-red {current_version}, but {latest_version} is available.")
        click.echo("Run 'pip install gator-red --upgrade' to update.\n")

if __name__ == '__main__':
    check_latest_version()
