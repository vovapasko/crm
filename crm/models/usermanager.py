from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from ..library.constants import SUPERUSER, ADMIN, MANAGER, GUEST


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_guest_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        group = Group.objects.filter(name=GUEST).first()

        return self.__create_user(email, password, group, **extra_fields)

    def create_manager_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        group = Group.objects.filter(name=MANAGER).first()

        return self.__create_user(email, password, group, **extra_fields)

    def create_admin_user(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        group = Group.objects.filter(name=ADMIN).first()

        return self.__create_user(email, password, group, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        group = Group.objects.filter(name=SUPERUSER).first()
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.__create_user(email, password, group, **extra_fields)

    def __create_user(self, email: str, password: str, group: str, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        user.groups.add(group)

        return user
