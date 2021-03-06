from drf_writable_nested import WritableNestedModelSerializer
from crm.serializers.contractors.contractor_publications_blacklist_serializer import ContractorPublicationsBlacklistSerializer
from crm.serializers.post_format_list_serializer import PostFormatListSerializer
from crm.models import Contractor
from crm.serializers.contractors.contractor_publications_list_serializer import ContractorPublicationsListSerializer
from crm.serializers.contractors.contractor_comment_list_serializer import ContractorCommentListSerializer


class ContractorSerializer(WritableNestedModelSerializer):
    postformatlist_set = PostFormatListSerializer(many=True, required=False, read_only=True)
    contractorpublicationslist_set = ContractorPublicationsListSerializer(many=True, required=False, read_only=True)
    contractorpublicationsblacklist_set = ContractorPublicationsBlacklistSerializer(many=True, required=False,
                                                                                    read_only=True)
    contractorcommentlist_set = ContractorCommentListSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Contractor
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1

    def create(self, validated_data):
        new_contractor = self.__create_contractor(validated_data)
        new_contractor.save()
        return new_contractor

    def __create_contractor(self, validated_data):
        return Contractor.objects.create_contractor(**validated_data)
