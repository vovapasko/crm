from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import Serializer
from rest_framework.serializers import EmailField
from crm.models import User
from django.http import Http404


class EmailRegisteredSerializer(Serializer):
    max_email_length = 150

    email = EmailField(max_length=max_email_length)

    def validate_email(self, email: str) -> str:
        try:
            get_object_or_404(User, email=email)
            return email
        except Http404:
            raise ValidationError(f"Email {email} is not registered")
