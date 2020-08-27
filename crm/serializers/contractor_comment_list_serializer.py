from rest_framework.serializers import ModelSerializer
from crm.models.contractor_comment_list import ContractorCommentList
from drf_writable_nested import WritableNestedModelSerializer


class ContractorCommentListSerializer(WritableNestedModelSerializer):
    class Meta:
        model = ContractorCommentList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
