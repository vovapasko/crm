from rest_framework import serializers
from crm.models.contractor_publications_blacklist import ContractorPublicationsBlacklist


class ContractorPublicationsBlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractorPublicationsBlacklist
        fields = "__all__"
        read_only_fields = [
            'date_created',
            'date_updated',
        ]
