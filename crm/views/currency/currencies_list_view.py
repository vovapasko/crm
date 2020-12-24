from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from crm.permissions import DjangoModelNoGetPermissions
from crm.views.base_view import BaseView
from rest_framework import generics
from crm.models import Currency
from crm.serializers import CurrencySerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from crm.library.constants import MESSAGE_JSON_KEY
from crm.paginations import StandardResultsSetPagination


class CurrenciesListView(BaseView, generics.ListCreateAPIView, DestroyAPIView, UpdateAPIView):
    queryset = Currency.objects.all().filter(is_archived=False).order_by('id')
    permission_classes = [IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = CurrencySerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        body params:
            name: [str] the name of the new currency
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return self.save_currency_and_response(serializer)

        return self.json_failed_response(
            message=dict(
                message="Creating currency failed"
            ),
            errors=serializer.errors
        )

    def save_currency_and_response(self, serializer: Serializer) -> Response:
        serializer.save()

        return self.json_success_response(
            message={MESSAGE_JSON_KEY: "Currency created successfully"},
            currency=serializer.data
        )

    is_archived_swagger_param = openapi.Parameter(
        name='is_archived',
        in_=openapi.IN_QUERY,
        description='Set this flag in body to true if you want to archive entity',
        required=False,
        type=openapi.TYPE_BOOLEAN
    )

    @swagger_auto_schema(manual_parameters=[is_archived_swagger_param],
                         responses={200: 'entity will be archived'})
    def put(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
