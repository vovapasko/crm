from drf_writable_nested import WritableNestedModelSerializer
from rest_framework.fields import SerializerMethodField
from crm.models.contractor_publications_list import ContractorPublicationsList
from crm.serializers.contractor_serializer import ContractorSerializer
from crm.serializers.contractor_comment_list_serializer import ContractorCommentListSerializer


class ContractorPublicationsListSerializer(WritableNestedModelSerializer):
    contractor = ContractorSerializer()
    comments = SerializerMethodField()

    class Meta:
        model = ContractorPublicationsList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1

    def get_comments(self, obj):
        data = ContractorCommentListSerializer(obj.contractor.contractorcommentlist_set.all(), many=True).data
        return data
