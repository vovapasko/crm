from drf_writable_nested import UniqueFieldsMixin
from rest_framework import serializers

from ....models import NewsEmail


class NewsEmailSerializer(UniqueFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = NewsEmail
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
