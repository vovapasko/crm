import requests
from django.conf import settings
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from email_app.library import constants
from email_app.library.gmail_helpers import credentials_to_dict
import os

if settings.DEBUG:
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

CLIENT_SECRETS_FILE = settings.CLIENT_SECRETS_FILE

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = settings.SENDING_EMAIL_SCOPE
API_SERVICE_NAME = constants.API_SERVICE_NAME
API_VERSION = constants.API_VERSION


def build_service(credentials: dict) -> Resource:
    credentials = google.oauth2.credentials.Credentials(**credentials)
    return googleapiclient.discovery.build(
        API_SERVICE_NAME, API_VERSION, credentials=credentials)


def start_authorize(par_state: str):
    current_dir = os.getcwd()
    path = os.path.join(current_dir, CLIENT_SECRETS_FILE)
    # Create flow instance to manage the OAuth 2.0 Authorization Grant Flow steps.
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        path, scopes=SCOPES)

    # The URI created here must exactly match one of the authorized redirect URIs
    # for the OAuth 2.0 client, which you configured in the API Console. If this
    # value doesn't match an authorized URI, you will get a 'redirect_uri_mismatch'
    # error.
    flow.redirect_uri = settings.GMAIL_API_REDIRECT_URI

    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true',
        state=par_state
    )

    # Store the state so the callback can verify the auth server response.

    return authorization_url, state


def finish_authorize(state: str, request_url: str) -> dict:
    # Specify the state when creating the flow in the callback so that it can
    # verified in the authorization server response.
    state = state

    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = settings.GMAIL_API_REDIRECT_URI
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request_url
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    return credentials_to_dict(credentials)


def has_credentials(user_id: str):
    pass


def get_credentials(user_id: str):
    pass


def revoke(user_id: str):
    '''user_id is normally an email'''
    if not has_credentials(user_id):
        return ('You need to <a href="/authorize">authorize</a> before ' +
                'testing the code to revoke credentials.')

    credentials = google.oauth2.credentials.Credentials(
        get_credentials(user_id))

    revoke = requests.post('https://oauth2.googleapis.com/revoke',
                           params={'token': credentials.token},
                           headers={'content-type': 'application/x-www-form-urlencoded'})

    status_code = getattr(revoke, 'status_code')
    if status_code == 200:
        return 'Credentials successfully revoked.'
    else:
        return 'An error occurred.'


def clear_credentials():
    # todo provide erasing credentials from DB
    pass
