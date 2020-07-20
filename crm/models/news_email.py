from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsEmail(AbstractBaseModel):
    email = models.EmailField(_('email address'), unique=True)
    template = models.TextField(help_text="Text for email template", null=True, blank=True)
    signature = models.TextField(help_text="Signature in the end of email", null=True, blank=True)

    def __str__(self):
        return self.email