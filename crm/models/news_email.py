from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class NewsEmail(AbstractBaseModel):
    codeword_length = 50

    email = models.EmailField(_('email address'), unique=True, null=False, blank=False)
    template = models.TextField(help_text="Text for email template", null=True, blank=True)
    signature = models.TextField(help_text="Signature in the end of email", null=True, blank=True)
    codeword = models.CharField(help_text="Additional information about holder of email",
                                max_length=codeword_length)

    def __str__(self):
        return f"{self.email} {self.codeword}"
