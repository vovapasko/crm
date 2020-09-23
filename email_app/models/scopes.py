from crm.models.abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Scopes(AbstractBaseModel):
    char_len = 200

    credentials = models.ForeignKey('Credentials',
                                    db_column='Credentials.id',
                                    name='credentials',
                                    on_delete=models.CASCADE)
    scope = models.CharField(_("scope"), max_length=char_len)

    def __str__(self):
        user = self.credentials.user_set.first()
        return f"Scope {self.scope} for {user}"
