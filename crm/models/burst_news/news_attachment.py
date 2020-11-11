from django.db import models

from ...models.abstract_base_model import AbstractBaseModel


class NewsAttachment(AbstractBaseModel):
    max_char_field_length = 200

    news = models.ForeignKey('News', on_delete=models.CASCADE)

    name = models.CharField(max_length=max_char_field_length)
    base_64 = models.TextField()
    type = models.CharField(max_length=max_char_field_length)

    def __str__(self):
        return self.name
