from crm.paginations import StandardResultsSetPagination
from crm.views.base_view import BaseView
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from crm.serializers.contractor_publications_list_serializer import ContractorPublicationsListSerializer
from crm.models import ContractorPublicationsList


class ContractorPublicationsView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractorPublicationsListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = ContractorPublicationsList.objects.all().order_by('id')
