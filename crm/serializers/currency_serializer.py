from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from crm.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = "__all__"
        readonly = ['date_created', 'date_updated']

    def validate_name(self, value: str) -> str:
        name_length = Currency.name_max_length
        if len(value) > name_length:
            raise ValidationError(f"Currency must be less than {name_length} symbols")
        return value
