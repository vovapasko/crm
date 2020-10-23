from rest_framework.serializers import BaseSerializer

from django.core.files.base import ContentFile
import base64
import six


class Base64AttachmentSerializer(BaseSerializer):
    def to_internal_value(self, attachment):
        data = attachment['base_64']
        file_name = attachment['name']
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

            complete_file_name = file_name

            return ContentFile(decoded_file, name=complete_file_name)
