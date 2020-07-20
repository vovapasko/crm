from ..library.constants import *

"""
Here is groups with permissions are stored
To add new group just add new key to groups dict. Key is a group name.
Vale to the group name is a list of permissions.

Don't forget to run upgrade_groups to commit changes
"""

groups = {
    SUPERUSER: [
    ],
    ADMIN: [
        CAN_INVITE_NEW_USER,
        CAN_DELETE_USER,
    ],
    MANAGER: [
        CAN_INVITE_NEW_USER,
        CAN_DELETE_USER,
    ],
    CLIENT: [
    ],
}
