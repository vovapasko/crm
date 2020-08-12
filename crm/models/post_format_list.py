from django.db import models
from .abstract_base_model import AbstractBaseModel
from django.utils.translation import gettext_lazy as _


class PostFormatList(AbstractBaseModel):
    max_post_format_length = 50
    default_value = 0

    contractor = models.ForeignKey('Contractor', on_delete=models.CASCADE)

    post_format = models.CharField(
        max_length=max_post_format_length,
        help_text='type of post for the news'
    )
    news_amount = models.PositiveIntegerField(
        _("news_amount"),
        help_text=_("Show amount of already published news"),
        default=default_value,
    )
    arranged_news = models.PositiveIntegerField(
        _("arranged news amount"),
        help_text=_("Shows amount of news which were arranged to publish per month"),
        default=default_value,
    )
    one_post_price = models.PositiveIntegerField(
        _("one post price"),
        help_text=_("Shows the price for one post of this type"),
        default=default_value
    )

    def __str__(self):
        return f"{self.post_format} - {self.contractor}"
