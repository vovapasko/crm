from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from crm.models.burst_news.news_wave_price_list import NewsWavePriceList
from crm.serializers import ContractorSerializer


class NewsWavePriceListSerializer(WritableNestedModelSerializer):
    news_wave = serializers.PrimaryKeyRelatedField(read_only=True)
    contractor = ContractorSerializer()

    class Meta:
        model = NewsWavePriceList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1
