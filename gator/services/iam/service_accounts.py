# gator/services/iam/service_accounts.py

import json
import base64 
import os
from googleapiclient import discovery
from OpenSSL import crypto

from gator.auth.credentials import load_credentials

def list_service_accounts(args):
    """Lists all service accounts for a given project."""
    creds = load_credentials(args)
    service = discovery.build('iam', 'v1', credentials=creds)

    resource = f'projects/{args.project_id}'
    request = service.projects().serviceAccounts().list(name=resource)
    response = request.execute()

    for account in response['accounts']:
        print(json.dumps(account, indent=4))

def download_service_account(args):
    creds = load_credentials(args)

    service = discovery.build('iam', 'v1', credentials=creds)

    service_accounts = args.service_account.split(',')

    for sa in service_accounts:
        key = create_service_account_key(service, args.project_id, sa)
        key['universe_domain'] = 'googleapis.com'
        key['auth_uri'] = 'https://accounts.google.com/o/oauth2/auth'
        key['token_uri'] = 'https://oauth2.googleapis.com/token'
        key['auth_provider_x509_cert_url'] = 'https://www.googleapis.com/oauth2/v1/certs'
        key['client_x509_cert_url'] = f"https://www.googleapis.com/robot/v1/metadata/x509/{sa.replace('@', '%40')}"
        save_service_account_key(args, key, sa) 

def create_service_account_key(service, project_id, service_account):
    resource = f'projects/{project_id}/serviceAccounts/{service_account}'
    body = {
        'keyAlgorithm': 'KEY_ALG_RSA_2048',
        'privateKeyType': 'TYPE_GOOGLE_CREDENTIALS_FILE'
    }
    request = service.projects().serviceAccounts().keys().create(name=resource, body=body)
    response = request.execute()

    key = json.loads(base64.b64decode(response['privateKeyData']))

    return key

def save_service_account_key(args, key, service_account):
    format = args.format.lower()
    directory = '../downloads'
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = f'{directory}/{service_account}.{format}'

    if format == 'json':
        with open(filename, 'w') as f:
            json.dump(key, f, indent=4)
    elif format == 'p12':
        p12 = crypto.PKCS12()
        pkey = crypto.load_privatekey(crypto.FILETYPE_PEM, key['private_key'])
        p12.set_privatekey(pkey)
        password = "notasecret"
        with open(filename, 'wb') as f:
            f.write(p12.export(passphrase=password))
    print(f'Service account key saved to {filename}.')
    if format in ['p12', 'P12']:
        print(f'The password for the .p12 file is: {password}')
