from . import Contractor, Hashtag
from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from .user import User


class NewsProject(AbstractBaseModel):
    max_project_name_len = 50
    max_client_name_len = 50

    name = models.CharField(
        _('project_name'),
        max_length=max_project_name_len,
        help_text="Stores the name for this particular news project"
    )
    budget = models.PositiveIntegerField(
        _('project_budget'),
        help_text="Budget for the project",
        default=0
    )
    client = models.CharField(
        _('client_name'),
        max_length=max_client_name_len,
        help_text="The name of the client for whom project is"
    )
    manager = models.ForeignKey(
        User,
        help_text="stores the key on User who created this project",
        on_delete=models.SET_NULL,
        null=True
    )

    hashtags = models.ManyToManyField(Hashtag, related_name='project_hashtags')
    contractors = models.ManyToManyField(Contractor, related_name='project_contractors')
    emails = models.ManyToManyField('NewsEmail', related_name='project_emails')

    def __str__(self):
        return f"{self.name} - {self.manager}"
