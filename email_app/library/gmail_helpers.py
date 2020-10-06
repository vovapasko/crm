import mimetypes
import os
import base64
import email
import os.path
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from crm.models import NewsEmail


def send_gmail_message(email_from: str, email_to: str, subject: str = None,
                       message_text: str = None, attachments: list = None):
    from email_app.library.gmail_utils import build_service
    try:
        test_email = NewsEmail.objects.get(email=email_from)  # this email has to exist
        email_from = test_email.email
        if attachments is None:
            message = create_message(
                sender=email_from,
                to=email_to,
                subject=subject,
                message_text=message_text
            )
        else:
            message = create_message_with_attachments(
                sender=email_from,
                to=email_to,
                subject=subject,
                message_text=message_text,
                files=attachments
            )
        credentials = test_email.gmail_credentials
        service = build_service(credentials=credentials.credentials_for_service())
        res = send_message(service=service, user_id=email_from, message=message)
        return res
    except Exception as e:
        raise e


def send_message(service, user_id, message):
    try:
        message = service.users().messages().send(userId=user_id, body=message).execute()

        print('Message Id: %s' % message['id'])

        return message
    except Exception as e:
        print('An error occurred: %s' % e)
        raise e


def create_message_with_attachments(sender, to, subject, message_text, files):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText(message_text)
    message.attach(msg)
    for file in files:
        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'

        main_type, sub_type = content_type.split('/', 1)

        if main_type == 'text':
            fp = open(file, 'rb')
            msg = MIMEText(fp.read().decode("utf-8"), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(file, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(file, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(file, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(file)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {
        'raw': raw_message.decode("utf-8")
    }


def get_messages(service, user_id) -> dict:
    try:
        return service.users().messages().list(userId=user_id, maxResults=10).execute()
    except Exception as error:
        raise error


def get_labels(service, user_id):
    try:
        return service.users().labels().list(userId=user_id).execute()
    except Exception as e:
        raise e


def get_message(service, user_id, msg_id):
    try:
        return service.users().messages().get(userId=user_id, id=msg_id, format='metadata').execute()
    except Exception as error:
        raise error


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


def create_draft(service, user_id, message_body):
    try:
        message = {'message': message_body}
        draft = service.users().drafts().create(userId=user_id, body=message).execute()

        print("Draft id: %s\nDraft message: %s" % (draft['id'], draft['message']))

        return draft
    except Exception as e:
        print('An error occurred: %s' % e)
        return None

    # Press the green button in the gutter to run the script.


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}
