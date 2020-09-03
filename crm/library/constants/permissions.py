from .views import APP_NAME


# permissions names
CAN_INVITE_NEW_USER = 'can_invite_new_user'
CAN_DELETE_USER = 'can_delete_user'

# names for permission_required in views
CAN_INVITE_NEW_USER_PERMISSION = APP_NAME + '.can_invite_new_user'
CAN_DELETE_USER_PERMISSION = APP_NAME + '.can_delete_user'

# groups
SUPERUSER = 'Superuser'
ADMIN = 'Admin'
MANAGER = 'Manager'
GUEST = 'Guest'

# list of priority groups for cascade permissions
GROUPS_FOR_CASCADE = [SUPERUSER, ADMIN, MANAGER, GUEST]

CODENAME = 'codename'
NAME = 'name'
CONTENT_TYPE = 'content_type'
REMOVE = 'remove'
ADD = 'add'
PERMISSIONS_PREFIXES = ['add', 'delete', 'view', 'change']
