from rest_framework import serializers
from crm.library.validators import validate_password
from crm.library.constants import FIRST_NAME, LAST_NAME, PASSWORD, PASSWORD_CONFIRM
from django.db.models import Model
from typing import Dict


class UserRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=50
    )
    last_name = serializers.CharField(
        max_length=50
    )
    password = serializers.CharField(
        validators=[validate_password]
    )
    password_confirm = serializers.CharField(
        validators=[validate_password],
    )

    def update(self, instance: Model, validated_data: Dict, is_confirmed: bool = True) -> None:
        instance.first_name = validated_data.get(FIRST_NAME, instance.first_name)
        instance.last_name = validated_data.get(LAST_NAME, instance.last_name)
        instance.set_password(validated_data.get(PASSWORD, instance.password))
        instance.is_confirmed = is_confirmed
        instance.save()

    def update_user(self, instance: Model, validated_data: Dict) -> None:
        self.update(instance, validated_data)

    def update_superuser(self, instance: Model, validated_data: Dict) -> None:
        self.update(instance, validated_data, is_confirmed=False)

    def validate(self, data: Dict) -> Dict:
        if data[PASSWORD] != data[PASSWORD_CONFIRM]:
            raise serializers.ValidationError("Passwords have to match")
        return data
