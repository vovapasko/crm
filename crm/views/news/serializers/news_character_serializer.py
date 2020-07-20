from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from typing import Dict
from ....models import NewsCharacter


class NewsCharacterSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=NewsCharacter()._meta.get_field('id'), required=False)

    class Meta:
        model = NewsCharacter
        fields = '__all__'
        readonly = ['date_created', 'date_updated']

    def validate(self, data: Dict) -> Dict:
        entity = NewsCharacter.objects.filter(pk=data.get('id')).first()
        if data.get('character') != entity.character:
            raise ValidationError("Invalid data in entity")
        return data
