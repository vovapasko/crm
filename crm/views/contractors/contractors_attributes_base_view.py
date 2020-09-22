# contains common methods for comments, publications and publications blacklist
from typing import Type
from django.db.models import Model
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from crm.paginations import StandardResultsSetPagination
from crm.permissions import DjangoModelNoGetPermissions
from crm.views.base_view import BaseView


class ContractorAttributesBaseView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated, DjangoModelNoGetPermissions]
    pagination_class = StandardResultsSetPagination
    get_request_param = 'contractor'

    def get_contractor_attribute_queryset(self, model: Type[Model]):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `contractor_id` query parameter in the URL.
        """
        queryset = model.objects.all()
        contractor_id = self.request.query_params.get(self.get_request_param, None)
        if contractor_id is not None:
            queryset = queryset.filter(contractor=contractor_id)
        return queryset.order_by('id')
