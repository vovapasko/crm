from django.db import models
from django.utils.translation import gettext_lazy as _
from crm.models.abstract_models import AbstractBaseModel, AbstractArchivedModel


class Hashtag(AbstractBaseModel, AbstractArchivedModel):
    name_max_length = 50

    name = models.CharField(_('name'), help_text="hashtag's name", max_length=name_max_length)

    def __str__(self):
        return f"{self.__class__.__name__}: {self.name}"

    def __repr__(self):
        return self.__str__()
