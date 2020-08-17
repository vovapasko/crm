from .abstract_base_model import AbstractBaseModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(AbstractBaseModel):
    number_max_length = 40
    name_max_length = 70
    emails_max_length = 70

    name = models.CharField(_("name"), help_text="client's name", max_length=name_max_length)
    numbers = models.CharField(_("numbers"), help_text="client's phone numbers", max_length=number_max_length)
    emails = models.CharField(_("emails"), help_text="client's emails", max_length=emails_max_length)

    price = models.PositiveIntegerField(
        verbose_name=_("price"),
        help_text="we don't understand for what it is"
    )
    amount_publications = models.PositiveIntegerField(
        verbose_name=_("amount_publish"),
        help_text="Displays how many publications we have to do for the client"
    )

    hashtags = models.ManyToManyField('Hashtag')
