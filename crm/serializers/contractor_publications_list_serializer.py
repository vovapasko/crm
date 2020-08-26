from rest_framework.serializers import ModelSerializer
from crm.models.contractor_publications_list import ContractorPublicationsList
from crm.serializers import ContractorSerializer, ContractorCommentListSerializer


class ContractorPublicationsListSerializer(ModelSerializer):
    contractor = ContractorSerializer()
    comments = ContractorCommentListSerializer(many=True)

    class Meta:
        model = ContractorPublicationsList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1
