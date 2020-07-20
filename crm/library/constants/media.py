# contains constants for folders where to store media files
from .views import APP_NAME
import os

users_avatar_dir = "users_pictures"
media_storage = os.path.join('main_app', users_avatar_dir)

default_avatar_filename = "avatar_2x.png"
default_avatar = os.path.join('main_app', default_avatar_filename)

news_attachments_dir = "news_attachments"
news_attachments_storage = os.path.join('main_app', news_attachments_dir)

wave_formation_attachments_dir = "wave_formation_attachments"
wave_formation_attachments_storage = os.path.join('main_app', wave_formation_attachments_dir)
