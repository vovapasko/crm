from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.http import request
from ..models import User


class LoginBackend(ModelBackend):
    def authenticate(self, request: request, username: str = None, password: str = None, **kwargs) -> User:
        user_model = get_user_model()

        if username is None:
            username = kwargs.get('email')

        try:
            user = user_model.objects.get(email=username)
        except user_model.DoesNotExist:
            raise ValueError({'email': 'No such email'})

        if user.check_password(password):
            return user

        raise ValueError({'password': 'Incorrect password'})
