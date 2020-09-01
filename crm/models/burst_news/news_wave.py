from django.db import models
from django.utils.translation import gettext_lazy as _
from .news_character import NewsCharacter
from .news_burst_method import NewsBurstMethod
from .wave_formation import WaveFormation
from crm.models import Hashtag, User
from .news import News
from crm.models.abstract_base_model import AbstractBaseModel
from crm.models.news_project import NewsProject


class NewsWave(AbstractBaseModel):
    wave_title_max_length = 200
    default_budget_value = 0
    max_post_format_length = 20

    title = models.CharField(_('title'),
                             max_length=wave_title_max_length,
                             help_text="Holds the name of the title for news wave"
                             )
    budget = models.PositiveIntegerField(_("budget"), default=default_budget_value)
    is_confirmed = models.BooleanField(_('confirmed'), default=False)
    post_format = models.CharField(
        max_length=max_post_format_length,
        help_text='type of post for the news wave'
    )

    news_character = models.ForeignKey(NewsCharacter, on_delete=models.PROTECT)
    burst_method = models.ForeignKey(NewsBurstMethod, on_delete=models.PROTECT)
    wave_formation = models.ForeignKey(WaveFormation, on_delete=models.SET_NULL, null=True, blank=True)
    project = models.ForeignKey(NewsProject, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    news_in_project = models.ManyToManyField(News)
    hashtags = models.ManyToManyField(Hashtag)

    def __str__(self):
        return self.title
