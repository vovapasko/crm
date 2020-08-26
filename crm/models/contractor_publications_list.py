from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from crm.models import ContractorCommentList


class ContractorPublicationsList(AbstractBaseModel):
    max_char_length = 200

    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)
    publish = models.CharField(
        _('publish'),
        help_text="Name of topic or edition which contractor publishes",
        max_length=max_char_length
    )
    not_publish = models.CharField(
        _('not_publish'),
        help_text="Name of topic or edition which contractor doesn't publish",
        max_length=max_char_length
    )
    comments = models.ForeignKey(ContractorCommentList, on_delete=models.CASCADE)

    def __str__(self):
        return self.contractor
