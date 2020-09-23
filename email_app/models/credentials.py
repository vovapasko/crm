import uuid

from crm.models.abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _

from email_app.models.credentials_manager import CredentialsManager


class Credentials(AbstractBaseModel):
    char_len = 200

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    token = models.CharField(_('token'), max_length=char_len)
    refresh_token = models.CharField(_('refresh_token'), max_length=char_len)
    token_uri = models.CharField(_('token_uri'), max_length=char_len)
    client_id = models.CharField(_('client_id'), max_length=char_len)
    client_secret = models.CharField(_('client_secret'), max_length=char_len)

    objects = CredentialsManager()
