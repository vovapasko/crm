from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from crm.serializers.hashtag_serializer import HashtagSerializer
from .news_email_serializer import NewsEmailSerializer
from crm.serializers.contractors import ContractorSerializer
from crm.serializers.client_serializer import ClientSerializer
from crm.models import NewsProject, User
from crm.serializers import UserSerializer
from rest_framework import serializers
from drf_writable_nested import WritableNestedModelSerializer


class NewsProjectSerializer(WritableNestedModelSerializer):
    # this field helps to get the request owner
    manager = UserSerializer(read_only=True)
    client = ClientSerializer()
    hashtags = HashtagSerializer(many=True)
    contractors = ContractorSerializer(many=True)
    emails = NewsEmailSerializer(many=True)
    manager_id = serializers.IntegerField(required=True)

    class Meta:
        model = NewsProject
        fields = '__all__'
        readonly = ['date_created', 'date_updated']
        depth = 1

    def create(self, validated_data: dict) -> NewsProject:
        # as if we don't have owner field in model we are going to create, we need to delete this field and remove it by manager field
        manager_id = validated_data.pop('manager_id', None)
        owner = User.objects.get(pk=manager_id)
        validated_data.update({'manager': owner})
        self.data.update({'manager': owner})
        return super().create(validated_data)

    def validate_emails(self, emails: list) -> list:
        if len(emails) < 1:
            raise ValidationError("Empty emails")
        return emails

    def validate_manager_id(self, id: int) -> int:
        try:
            user = get_object_or_404(User, pk=id)
        except Http404:
            raise ValidationError(f"User with id {id} does not exist")
        return id
