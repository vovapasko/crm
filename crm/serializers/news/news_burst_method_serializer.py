from rest_framework import serializers

from crm.models import NewsBurstMethod


class NewsBurstMethodSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=NewsBurstMethod()._meta.get_field('id'))

    class Meta:
        model = NewsBurstMethod
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
