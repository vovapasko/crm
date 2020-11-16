import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import six
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from crm.models import WaveFormationAttachment, NewsEmail
from email_app.library.gmail_helpers import send_gmail_message_from_wave, send_message
from pathlib import Path

from email_app.library.gmai_api_view_utils import build_service


def from_base64_to_content_file(base64_str: str, filename: str):
    data = base64_str
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_file')

        return ContentFile(decoded_file, name=filename)


def create_message_with_attachments(to, sender, subject):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject

    msg = MIMEText('message_text', 'html')
    message.attach(msg)

    wv_file = WaveFormationAttachment.objects.last()
    content_type = wv_file.type
    if content_type is None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)
    fp = from_base64_to_content_file(wv_file.base_64, wv_file.name)
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
    filename = wv_file.name
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_string().encode("utf-8"))
    return {'raw': raw_message.decode("utf-8")}


class Command(BaseCommand):
    def handle(self, *args, **options):
        # file1 = Path('README.md')
        # file2 = Path('requirements.txt')
        # text = 'Hello from Django with attachments'
        # subject = 'Test Django'
        # mail_from = 'mailfrom@gmail.com'
        # mail_to = 'mailto@gmail.com'
        # send_gmail_message(
        #     email_from=mail_from,
        #     email_to=mail_to,
        #     subject=subject,
        #     message_text=text,
        #     attachments=[file1, file2]
        # )
        email_from = NewsEmail.objects.get(email='petro307302@gmail.com')
        message = create_message_with_attachments(to='supermariob2019@gmail.com',
                                                  sender=email_from.email,
                                                  subject='Test Flight')
        self.send_message(test_email=email_from,
                          email_from=email_from.email,
                          message=message)

    def send_message(self, test_email, email_from: str, message):
        credentials = test_email.gmail_credentials
        service = build_service(credentials=credentials.credentials_for_service())
        res = send_message(service=service, user_id=email_from, message=message)
        print(res)
