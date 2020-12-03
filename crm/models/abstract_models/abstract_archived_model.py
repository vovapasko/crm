from django.db import models


class AbstractArchivedModel(models.Model):
    is_archived = models.BooleanField(default=False)

    class Meta:
        abstract = True
