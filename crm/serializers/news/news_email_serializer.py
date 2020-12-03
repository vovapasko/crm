from drf_writable_nested import WritableNestedModelSerializer
from crm.models import NewsEmail


class NewsEmailSerializer(WritableNestedModelSerializer):
    class Meta:
        model = NewsEmail
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
