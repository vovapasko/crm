from ...apps import CrmConfig

FIRST_NAME = 'first_name'
LAST_NAME = 'last_name'
EMAIL = 'email'
PASSWORD = 'password'
PASSWORD_CONFIRM = 'password_confirm'
HTTP_HOST = 'HTTP_HOST'
ID = 'id'
DATA = 'data'
GROUP_LIST = 'group_list'
USER = 'user'
GROUP = 'group'
DELETE_LINK = 'delete_link'
CONFIRMED = 'confirmed'
ACCESS = 'access'
REFRESH = 'refresh'
TOKEN = 'token'
SUCCESS = 'success'
ERRORS = 'errors'
SIGNATURE = 'signature'
PERMISSION = 'permission'
USER_ID = 'user_id'
MESSAGE_JSON_KEY = "message"

APP_NAME = CrmConfig.name

# email templates
PASSWORD_CHANGE_EMAIL = f'{APP_NAME}/email/password_change_confirm.txt'
REGISTER_NEW_USER_EMAIL = f'{APP_NAME}/email/invite_new_user.txt'
CHANGE_GROUP_EMAIL = f'{APP_NAME}/email/change_group.txt'
FORGOT_PASSWORD_EMAIL_TEMPLATE = f'{APP_NAME}/email/forgot_password.txt'

# api endpoints
HOME_API = f'{APP_NAME}:home'
LOGIN_API = f'{APP_NAME}:login'
PROFILE_API = f'{APP_NAME}:profile'
CHANGE_PASSWORD_API = f'{APP_NAME}:change-pass'
USER_CONFIRM_API = f'{APP_NAME}:confirm-user'
# links
LOCAL_SERVER = "127.0.0.1:4200"
DEV_SERVER = "https://dmc-front.herokuapp.com"
PRODUCTION_SERVER = "https://dmc-crm-production-frontend.herokuapp.com"
INVITE_NEW_USER_LINK = "account/signup"
CHANGE_PASSWORD_LINK = "account/change-password"
FORGOT_PASSWORD_LINK = "account/forgot-password"
