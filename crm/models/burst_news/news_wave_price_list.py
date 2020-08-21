from crm.models.abstract_base_model import AbstractBaseModel
from django.db import models
from crm.models import Contractor
from django.utils.translation import gettext_lazy as _


class NewsWavePriceList(AbstractBaseModel):
    contractor = models.ForeignKey(Contractor, on_delete=models.PROTECT)
    price = models.PositiveIntegerField(_('price'))
