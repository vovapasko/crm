from django.db import models
from ..abstract_base_model import AbstractBaseModel


class NewsCharacter(AbstractBaseModel):
    character_max_length = 20
    character = models.CharField(
        max_length=character_max_length,
        default='standard',
    )

    def __str__(self):
        return self.character
