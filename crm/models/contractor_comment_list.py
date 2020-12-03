from crm.models.abstract_models.abstract_base_model import AbstractBaseModel
from django.db import models


class ContractorCommentList(AbstractBaseModel):
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)
    comment = models.TextField(help_text="Contains comment to this contractor", blank=True)
