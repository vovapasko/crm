from rest_framework.exceptions import ValidationError

from .change_password_serializer import ChangePasswordSerializer
from rest_framework.serializers import CharField
from django.contrib.auth.tokens import default_token_generator

from ...library.helpers.views import unconvert_uid
from ...models import User


class ConfirmPasswordSerializer(ChangePasswordSerializer):
    uid = CharField()
    token = CharField()

    def validate(self, data):
        user = User.objects.get(id=unconvert_uid(data.get('uid')))
        if default_token_generator.check_token(user, data.get('token')):
            return data
        raise ValidationError("Incorrect token or uid")
