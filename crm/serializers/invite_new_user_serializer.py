from rest_framework import serializers


class InviteNewUserSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    group = serializers.CharField(required=True)
