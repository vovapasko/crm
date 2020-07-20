from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ....library.validators import check_positive_numbers
from ....models import PostFormatList


class PostFormatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFormatList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]

    def validate_news_amount(self, value):
        check_positive_numbers(value, "News amount")
        return value

    def validate_arranged_news(self, value):
        check_positive_numbers(value, "Arranged news number")
        return value

    def validate_one_post_price(self, value):
        check_positive_numbers(value, "One post price")
        return value
