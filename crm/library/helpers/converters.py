from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from typing import Union

import six
from django.core.files.base import ContentFile
import base64


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


def convert_base64_to_mime_attachment(file_name: str, file_base64: str, file_type: Union[str, None]) -> MIMEBase:
    content_type = file_type

    if content_type is None:
        content_type = 'application/octet-stream'

    main_type, sub_type = content_type.split('/', 1)
    fp = from_base64_to_content_file(file_base64, file_name)
    if main_type == 'text':
        mime_part = MIMEText(fp.read().decode("utf-8"), _subtype=sub_type)
        fp.close()
    elif main_type == 'image':
        mime_part = MIMEImage(fp.read(), _subtype=sub_type)
        fp.close()
    elif main_type == 'audio':
        mime_part = MIMEAudio(fp.read(), _subtype=sub_type)
        fp.close()
    else:
        mime_part = MIMEBase(main_type, sub_type)
        mime_part.set_payload(fp.read())
        fp.close()
    mime_part.add_header('Content-Disposition', 'attachment', filename=file_name)
    return mime_part
