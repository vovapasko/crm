from django.db import models

from .. import Contractor
from ..news_email import NewsEmail
from crm.models.abstract_models import AbstractBaseModel, AbstractArchivedModel


class NewsManager(models.Manager):
    def create(self, **data):
        news = News(
            email=data['email'],
            title=data['title'],
            content=data['content']
        )
        news.save()

        attachments = data.get('attachments', None)
        if attachments:
            for attachment in attachments:
                attachment.news = news
                attachment.save()
        return news


class News(AbstractBaseModel, AbstractArchivedModel):
    title_max_length = 30

    email = models.ForeignKey(NewsEmail, on_delete=models.PROTECT)
    title = models.CharField(max_length=title_max_length)
    content = models.TextField()
    contractors = models.ManyToManyField(Contractor)

    objects = NewsManager()

    def __str__(self):
        return f'News {self.id} for {self.email} - {str(self.title[:10])}'
