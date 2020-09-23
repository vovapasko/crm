from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from email_app.models import Credentials
from .usermanager import UserManager
from ..library.constants.media import default_avatar, media_storage
from typing import List


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    avatar = models.ImageField(
        default=default_avatar,
        upload_to=media_storage
    )

    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_updated = models.DateTimeField(_('date updated'), auto_now=True)

    is_active = models.BooleanField(_('active'), default=True)
    is_confirmed = models.BooleanField(_('confirmed'), default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_superuser = models.BooleanField(_('superuser'), default=False)

    gmail_credentials = models.ForeignKey(Credentials, db_column='Credentials.id',
                                          name='gmail_credentials',
                                          on_delete=models.CASCADE, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS: List = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def __str__(self):
        return f"{self.__class__.__name__}: {self.email}"

    def __repr__(self):
        return self.__str__()

    def delete(self, using=None, keep_parents=False):
        self.avatar.delete()  # delete avatar instance from S3
        super().delete(using=None, keep_parents=False)
