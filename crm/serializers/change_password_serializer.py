from rest_framework import serializers
from crm.library.validators import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )
