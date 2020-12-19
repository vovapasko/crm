from django.db import models
from crm.models.abstract_models.abstract_base_model import AbstractBaseModel


class NewsBurstMethod(AbstractBaseModel):
    method = models.CharField(
        max_length=50,
        default='direct',
        help_text='format how to burst the news'
    )

    def __str__(self):
        return self.method
