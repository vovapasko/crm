from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractorPublicationsList(AbstractBaseModel):
    max_char_length = 200

    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)
    publish = models.CharField(
        _('publish'),
        help_text="Name of topic or edition which contractor publishes",
        max_length=max_char_length,
        blank=True,
    )

    def __str__(self):
        return f"Publications list of {self.contractor.editor_name}"
