from ..abstract_base_model import AbstractBaseModel
from django.db import models


class WaveFormationManager(models.Manager):
    def create(self, **data):
        wf = WaveFormation(
            email=data['email'],
            content=data['content']
        )
        wf.save()

        attachments = data.get('attachments', None)
        if attachments:
            for attachment in attachments:
                attachment.wave_formation = wf
                attachment.save()
        return wf


class WaveFormation(AbstractBaseModel):
    email = models.ForeignKey('NewsEmail', on_delete=models.PROTECT)
    content = models.TextField()

    objects = WaveFormationManager()

    def __str__(self):
        return f'{self.email} - {str(self.content)[:10]}'
