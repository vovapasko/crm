from rest_framework.serializers import ModelSerializer
from crm.models.contractor_comment_list import ContractorCommentList
from rest_framework import serializers


class ContractorCommentListSerializer(ModelSerializer):
    contractor = serializers.PrimaryKeyRelatedField

    class Meta:
        model = ContractorCommentList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
