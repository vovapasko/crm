### THIS FILE CONTAINS FUNCTIONS FOR INTERACTION BETWEEN GMAIL_API AND VIEWS

from typing import List, Union
from django.conf import settings
import google.oauth2.credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
from googleapiclient.discovery import Resource
from crm.models import NewsEmail
from email_app.library import constants
from email_app.library.gmail_api import get_messages, get_labels, get_profile, \
    get_message_with_metadata, get_raw_message, trash_message, untrash_message, \
    get_full_message, delete_message, list_messages_with_label, get_attachment, send_message
from email_app.library.gmail_helpers import credentials_to_dict, create_message, create_message_with_attachments
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
    print(f"Redirect uri {flow.redirect_uri}")
    # Use the authorization server's response to fetch the OAuth 2.0 tokens.
    authorization_response = request_url
    print(f"Authorization response {authorization_response}")
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials
    print('----------')
    print(credentials.__dict__)
    return credentials_to_dict(credentials)


def get_gmail_messages(email: NewsEmail, pagination: int, next_page_token: str = None) -> dict:
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    messages = get_messages(service=service, user_id=email.email, pagination_param=pagination,
                            page_token=next_page_token)
    return add_metadata_to_messages(service=service, email=email.email, messages=messages)


def add_metadata_to_messages(service, email: str, messages: dict):
    lst = messages.get('messages')
    if lst is None:
        return {}
    for _, i in zip(lst, range(len(lst))):
        message = get_message_with_metadata(service, email, _.get('id'))
        messages.get('messages')[i] = message
    return messages


def get_gmail_labels(email: NewsEmail) -> dict:
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    return get_labels(service=service, user_id=email.email)


def get_gmail_profile(email: NewsEmail) -> dict:
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    profile = get_profile(service=service, user_id=email.email)
    return profile


def get_raw_gmail_message(email: NewsEmail, message_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    message = get_raw_message(service=service, user_id=email.email, msg_id=message_id)
    return message


def get_full_gmail_message(email: NewsEmail, message_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    message = get_full_message(service=service, user_id=email.email, msg_id=message_id)
    return message


def trash_gmail_message(email: NewsEmail, message_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    message = trash_message(service=service, user_id=email.email, message_id=message_id)
    return message


def untrash_gmail_message(email: NewsEmail, message_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    message = untrash_message(service=service, user_id=email.email, message_id=message_id)
    return message


def remove_gmail_message(email: NewsEmail, message_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    message = delete_message(service=service, user_id=email.email, message_id=message_id)
    return message


def filter_label_gmail_message(email: NewsEmail, labels: List[str]):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    messages = list_messages_with_label(service=service, user_id=email.email, label_ids=labels)
    return add_metadata_to_messages(service=service, email=email.email, messages=messages)


def get_gmail_attachment(email: NewsEmail, message_id: str, attachment_id: str):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    attachment = get_attachment(service, user_id=email.email, message_id=message_id,
                                attachment_id=attachment_id)
    return attachment


def send_gmail_message(email: NewsEmail, email_to: str, subject: str, message_text: str,
                       attachments: Union[list, None], cc: str = None):
    creds = email.gmail_credentials.credentials_for_service()
    service = build_service(credentials=creds)
    user_id = email.email
    if attachments is None:
        message = create_message(sender=user_id, to=email_to, subject=subject, message_text=message_text, cc=cc)
    else:
        message = create_message_with_attachments(sender=user_id, to=email_to, subject=subject,
                                                  message_text=message_text, files=attachments, cc=cc)
    message = send_message(service, user_id=user_id, message=message)
    return message
