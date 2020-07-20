from django.contrib.contenttypes.models import ContentType
from ..models import User
from ..library.constants import *

"""
Here is permissions are stored
To add new permission just add new key to permissions dict. Key must be the same as codename of permission.
The value of the key is another dict with next keys:
    - codename of the permission
    - name of the permission
    - content_type of permission

Don't forget to add codename to the library.constants.permissions
"""

user_content_type = ContentType.objects.get_for_model(User)

permissions = {
    CAN_INVITE_NEW_USER: {
        CODENAME: CAN_INVITE_NEW_USER,
        NAME: 'Can invite new users cascade down',
        CONTENT_TYPE: user_content_type
    },
    CAN_DELETE_USER: {
        CODENAME: CAN_DELETE_USER,
        NAME: 'Can delete users cascade down',
        CONTENT_TYPE: user_content_type
    }
}
