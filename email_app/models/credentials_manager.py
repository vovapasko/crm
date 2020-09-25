from typing import List

from django.db.models import Manager
from typing import TYPE_CHECKING

from django.conf import settings
from email_app.models.scopes import Scopes

if TYPE_CHECKING:
    import email_app.models.Credentials


class CredentialsManager(Manager):
    def create_credentials(self, email: str, token: str, refresh_token: str,
                           token_uri: str, client_id: str,
                           client_secret: str, scopes: list) -> 'Credentials':
        credentials = self.create(
            token=token,
            refresh_token=refresh_token,
            token_uri=token_uri,
            client_id=client_id,
            client_secret=client_secret
        )
        self.__create_scope(credentials, scopes)
        email.gmail_credentials = credentials
        email.save()
        return credentials

    def __create_scope(self, credentials: 'Credentials', scopes: list) -> List[Scopes]:
        return Scopes.objects.bulk_create([Scopes(credentials=credentials, scope=scope) for scope in scopes])
