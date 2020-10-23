from ..abstract_base_model import AbstractBaseModel
from django.db import models

from ...library.constants.media import wave_formation_attachments_storage


class WaveFormationAttachment(AbstractBaseModel):
    wave_formation = models.ForeignKey('WaveFormation', on_delete=models.CASCADE)
    file = models.FileField(upload_to=wave_formation_attachments_storage)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()  # delete file instance on S3 Bucket
        super().delete(using=None, keep_parents=False)

    def __str__(self):
        return self.file.name
