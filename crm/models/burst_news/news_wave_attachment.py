from ..abstract_base_model import AbstractBaseModel
from django.db import models


class NewsWaveAttachment(AbstractBaseModel):
    max_char_field_length = 200

    name = models.CharField(max_length=max_char_field_length)
    base_64 = models.TextField()
    type = models.CharField(max_length=max_char_field_length)

    news = models.ForeignKey('News', on_delete=models.CASCADE, blank=True, null=True)
    wave_formation = models.ForeignKey('WaveFormation', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.name
