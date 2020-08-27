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

    get_request_param = 'contractor'

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `contractor_id` query parameter in the URL.
        """
        queryset = ContractorPublicationsList.objects.all()
        contractor_id = self.request.query_params.get(self.get_request_param, None)
        if contractor_id is not None:
            queryset = queryset.filter(contractor=contractor_id)
        return queryset.order_by('id')
