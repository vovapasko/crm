from django.core import signing
import os

from django.template.loader import render_to_string
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.signing import BadSignature

from ..constants import PRODUCTION_SERVER
from ...library.constants import DATA, ID, LOCAL_SERVER, DEV_SERVER
from django.core.exceptions import ObjectDoesNotExist
from typing import Dict, List
from ...models import User
from django.conf import settings


def decode_singing_dict(data: Dict) -> Dict:
    """
    decode signed dict
    :param data: signed dict
    :return: dict of decoded data
    """
    if data is None:
        return dict()

    data_decoded = {}

    for key, value in signing.loads(data).items():
        data_decoded[key] = value

    return data_decoded


def send_dmc_email(template: str, receivers: List[str], subject: str = None, **kwargs) -> None:
    """
    send letter from email registered in settings.py
    :param template: template for render
    :param receivers: list of receivers' emails
    :param subject: subject for email, optional
    :param kwargs: for template render
    """
    if subject is None:
        subject = 'DMC support auto email'

    message = Mail(from_email=settings.EMAIL_HOST_USER,
                   to_emails=receivers,
                   subject=subject,
                   plain_text_content=render_to_string(template, kwargs))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        raise e


def generate_token_dict(user: User) -> Dict:
    refresh = RefreshToken.for_user(user)

    return dict(
        refresh=str(refresh),
        access=str(refresh.access_token),
    )


def get_id_or_exception(**kwargs) -> dict:
    """
    Return user_id if this user was correctly encoded in link.
    Otherwise return exception
    """
    try:
        return decode_singing_dict(kwargs[DATA])[ID]
    except BadSignature:
        raise ObjectDoesNotExist


def format_link(link):
    server = DEV_SERVER
    if settings.DEBUG:
        server = LOCAL_SERVER
    if settings.PRODUCTION:
        server = PRODUCTION_SERVER
    return f"{server}/{link}"
