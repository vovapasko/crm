from ..abstract_base_model import AbstractBaseModel
from django.db import models


class WaveFormation(AbstractBaseModel):
    email = models.ForeignKey('NewsEmail', on_delete=models.PROTECT)
    content = models.TextField()
