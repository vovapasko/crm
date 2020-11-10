from ..abstract_base_model import AbstractBaseModel
from django.db import models

from ...library.constants.media import wave_formation_attachments_storage


class WaveFormationAttachment(AbstractBaseModel):
    max_char_field_length = 200

    wave_formation = models.ForeignKey('WaveFormation', on_delete=models.CASCADE)
    name = models.CharField(max_length=max_char_field_length)
    base_64 = models.TextField()
    type = models.CharField(max_length=max_char_field_length)


    def __str__(self):
        return self.name
