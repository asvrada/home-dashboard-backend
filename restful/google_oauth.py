from google.auth.transport import requests
from google.oauth2 import id_token

CLIENT_ID = "508553430731-3sjtbacd9na89labelop5fii28h4ho1m.apps.googleusercontent.com"


def get_google_user_from_google_token(token):
    try:
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')

        # ID token is valid. Get the user's Google Account ID from the decoded token.
        return idinfo
    except ValueError as err:
        # Invalid token
        print(err)
        return None
