from django.db import models

from ...library.constants.media import news_attachments_storage

from ...models.abstract_base_model import AbstractBaseModel


class NewsAttachment(AbstractBaseModel):
    news = models.ForeignKey('News', on_delete=models.CASCADE)
    file = models.FileField(upload_to=news_attachments_storage)

    def delete(self, using=None, keep_parents=False):
        self.file.delete()  # delete file instance on S3 Bucket
        super().delete(using=None, keep_parents=False)
