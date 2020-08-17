from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from crm.models import Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"
        readonly = ['date_created', 'date_updated']

    def validate_name(self, value: str) -> str:
        name_length = Hashtag.name_max_length
        if len(value) > name_length:
            raise ValidationError(f"Hashtag must be less than {name_length} symbols")
        return value
