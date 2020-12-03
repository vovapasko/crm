from django.db import models
from django.utils.translation import gettext_lazy as _
from crm.models.abstract_models import AbstractBaseModel, AbstractArchivedModel
from .contractor_manager import ContractorManager


class Contractor(AbstractBaseModel, AbstractArchivedModel):
    editor_name = models.CharField(_('editor name'), max_length=100)
    contact_person = models.CharField(_('contact person'), max_length=100)
    phone_number = models.CharField(_("phone number"), max_length=20)
    email = models.EmailField(_("email"))

    objects = ContractorManager()

    def __str__(self):
        return self.editor_name
