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

    def get_credentials(self) -> dict:
        return {
            "token": self.token,
            "refresh_token": self.refresh_token,
            "token_uri": self.token_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": self.scopes_set.all(),
            "email": self.newsemail_set.first()  # because credentials can belong only to one email
        }

    def __str__(self):
        email = self.get_credentials().get('email')
        return f"{id} - {email}"

    def credentials_for_service(self) -> dict:
        prepared_scope = [scope.get_scope() for scope in self.scopes_set.all()]
        return {
            "token": self.token,
            "refresh_token": self.refresh_token,
            "token_uri": self.token_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scopes": prepared_scope,
        }
