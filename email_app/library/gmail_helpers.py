import base64
import email
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Union

from crm.library.helpers import from_base64_to_content_file
from crm.models import NewsEmail
from email_app.library.gmail_api import send_message


def send_gmail_message_from_wave(email_from: str, email_to: str, subject: str = None,
                                 message_text: str = None, attachments: list = None):
    from email_app.library.gmai_api_view_utils import build_service
    try:
        test_email = NewsEmail.objects.get(email=email_from)  # this email has to exist
        email_from = test_email.email
        message = build_message_from_wave(email_from=email_from, email_to=email_to, subject=subject,
                                          message_text=message_text,
                                          attachments=attachments)
        credentials = test_email.gmail_credentials
        service = build_service(credentials=credentials.credentials_for_service())
        res = send_message(service=service, user_id=email_from, message=message)
        return res
    except Exception as e:
        raise e


def build_message_from_wave(email_from: str, email_to: str, subject: str,
                            message_text: str, attachments: Union[list, None]) -> Union[MIMEBase, dict]:
    if attachments is None:
        message = create_message(
            sender=email_from,
            to=email_to,
            subject=subject,
            message_text=message_text
        )
    else:
        message = create_message_with_attachments_from_wave(
            sender=email_from,
            to=email_to,
            subject=subject,
            message_text=message_text,
            files=attachments
        )
    return message


def create_message_with_attachments_from_wave(sender, to, subject, message_text, files):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text, 'html')
    message.attach(msg)
    for file in files:
        content_type = file.type

        if content_type is None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)
        fp = from_base64_to_content_file(file.base_64, file.name)
        if main_type == 'text':
            msg = MIMEText(fp.read().decode("utf-8"), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = file.name
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


# todo complete this function
def create_message_with_attachments(sender, to, subject, message_text, files):
    pass


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text, 'html')
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def get_mime_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id,
                                                 format='raw').execute()
        print('Message snippet: %s' % message['snippet'])
        msg_str = base64.urlsafe_b64decode(message['raw'].encode("utf-8")).decode("utf-8")
        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except Exception as error:
        print('An error occurred: %s' % error)


def get_attachments(service, user_id, msg_id, store_dir):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()

        for part in message['payload']['parts']:
            if (part['filename'] and part['body'] and part['body']['attachmentId']):
                attachment = service.users().messages().attachments().get(id=part['body']['attachmentId'],
                                                                          userId=user_id, messageId=msg_id).execute()

                file_data = base64.urlsafe_b64decode(attachment['data'].encode('utf-8'))
                path = ''.join([store_dir, part['filename']])

                f = open(path, 'wb')
                f.write(file_data)
                f.close()
    except Exception as error:
        print('An error occurred: %s' % error)


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
