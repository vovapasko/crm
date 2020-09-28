from django.core.exceptions import ValidationError
from rest_framework import serializers
from crm.models import NewsEmail
from django.db.models import ObjectDoesNotExist


class GmailClearCredentialsSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email: str) -> str:
        try:
            news_email = NewsEmail.objects.get(email=email)
            if news_email.gmail_credentials is None:
                raise ValidationError(f"Email {email} is not logged in. Nothing to clear")
        except ObjectDoesNotExist:
            raise ValidationError(f"Email {email} does not exist")
        return email
