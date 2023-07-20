import requests

def is_token_expired(token):
    """
    Validates if an access token is expired.
    """
    response = requests.get(
        'https://www.googleapis.com/oauth2/v2/userinfo',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.status_code != 200  # If status code is not 200, then token is likely expired
