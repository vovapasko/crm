from crm.models.abstract_models.abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsWavePriceList(AbstractBaseModel):
    news_wave = models.ForeignKey('NewsWave', on_delete=models.PROTECT)
    contractor = models.ForeignKey('Contractor', on_delete=models.PROTECT)
    price = models.PositiveIntegerField(_('price'))

    def __str__(self):
        return f"{self.news_wave.title} - {self.contractor.editor_name} - {self.price}"
