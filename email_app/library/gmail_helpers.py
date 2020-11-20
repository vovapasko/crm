import base64
import email
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union, List, Dict

from crm.library.helpers import from_base64_to_content_file
from crm.library.helpers.converters import convert_base64_to_mime_attachment
from crm.models import NewsEmail
from email_app.library.gmail_api import send_message


def send_gmail_message_from_wave(email_from: str, email_to: str,
                                 subject: str,
                                 message_text: str,
                                 attachments: list = None,
                                 template: str = None,
                                 signature: str = None):
    from email_app.library.gmai_api_view_utils import build_service
    try:
        test_email = NewsEmail.objects.get(email=email_from)  # this email has to exist
        email_from = test_email.email
        message = build_message_from_wave(email_from=email_from,
                                          email_to=email_to,
                                          subject=subject,
                                          message_text=message_text,
                                          attachments=attachments,
                                          template=template,
                                          signature=signature)
        credentials = test_email.gmail_credentials
        service = build_service(credentials=credentials.credentials_for_service())
        res = send_message(service=service, user_id=email_from, message=message)
        return res
    except Exception as e:
        raise e


def build_message_from_wave(email_from: str, email_to: str, subject: str,
                            message_text: str,
                            attachments: Union[list, None] = None,
                            template: str = None,
                            signature: str = None
                            ) -> Union[MIMEBase, dict]:
    message = create_message_from_wave(
        sender=email_from,
        to=email_to,
        subject=subject,
        message_text=message_text,
        files=attachments,
        template=template,
        signature=signature
    )
    return message


def create_mime_message_body(message: MIMEBase,
                             message_text: str,
                             template: str = None,
                             signature: str = None) -> None:
    if template is not None:
        template_mime = MIMEText(template, 'html')
        message.attach(template_mime)
    msg = MIMEText(message_text, 'html')
    message.attach(msg)
    if signature is not None:
        signature_mime = MIMEText(signature, 'html')
        message.attach(signature_mime)


def create_message_from_wave(sender: str,
                             to: str,
                             subject: str,
                             message_text: str,
                             files: Union[list, None] = None,
                             template: str = None,
                             signature: str = None) -> dict:
    message = create_mime_signature(sender, to, subject)

    create_mime_message_body(message, message_text, template, signature)

    if files:
        for file in files:
            msg = convert_base64_to_mime_attachment(file_type=file.type, file_name=file.name,
                                                    file_base64=file.base_64)

            message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


def create_mime_signature(sender: str, to: str, subject: str, cc: str = None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc is not None:
        message['Cc'] = cc
    return message


def create_message_with_attachments(sender, to: str, subject: str, message_text: str,
                                    files: Union[List[Dict[str, str, str]], None] = None,
                                    cc: str = None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc is not None:
        message['Cc'] = cc

    msg = MIMEText(message_text, 'html')
    message.attach(msg)
    for file in files:
        msg = convert_base64_to_mime_attachment(file_type=file.get('type'), file_name=file.get('name'),
                                                file_base64=file.get('base_64'))
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


def create_message(sender: str, to: str, subject: str,
                   message_text: str,
                   cc: Union[str, None] = None,
                   template: str = None,
                   signature: str = None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if cc is not None:
        message['Cc'] = cc
    if template is not None:
        template_mime = MIMEText(template, 'html')
        message.attach(template_mime)
    message_text_mime = MIMEText(message_text, 'html')
    message.attach(message_text_mime)
    if signature is not None:
        signature_mime = MIMEText(signature, 'html')
        message.attach(signature_mime)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
