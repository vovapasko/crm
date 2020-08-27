from drf_writable_nested import WritableNestedModelSerializer
from crm.models.contractor_publications_list import ContractorPublicationsList



class ContractorPublicationsListSerializer(WritableNestedModelSerializer):
    class Meta:
        model = ContractorPublicationsList
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
        depth = 1
