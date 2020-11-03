import six
from django.core.files.base import ContentFile


def from_base64_to_content_file(base64: str, filename: str):
    data = base64
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
