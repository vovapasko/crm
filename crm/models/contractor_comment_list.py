from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class ContractorCommentList(AbstractBaseModel):
    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)
    comment = models.TextField()
