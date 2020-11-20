from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers
from rest_framework.serializers import Serializer

from crm.models import NewsEmail


class EmailSerialiser(Serializer):
    email = serializers.EmailField()

    def validate_email(self, email: str) -> str:
        try:
            NewsEmail.objects.get(email=email)
        except ObjectDoesNotExist:
            raise ValidationError(f"Email {email} does not exist")
        return email
