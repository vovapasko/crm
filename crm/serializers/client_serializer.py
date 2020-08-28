from drf_writable_nested import WritableNestedModelSerializer
from crm.models import Client
from crm.serializers.news import HashtagSerializer


class ClientSerializer(WritableNestedModelSerializer):
    hashtags = HashtagSerializer(many=True)

    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1
