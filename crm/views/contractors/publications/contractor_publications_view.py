from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response

from crm.models import ContractorPublicationsList
from crm.serializers import ContractorPublicationsListSerializer
from crm.views.contractors.contractors_attributes_base_view import ContractorAttributesBaseView


class ContractorPublicationsView(ContractorAttributesBaseView):
    serializer_class = ContractorPublicationsListSerializer

    test_param = openapi.Parameter(ContractorAttributesBaseView.get_request_param, openapi.IN_QUERY,
                                   description="get publications list for concrete contractor",
                                   type=openapi.TYPE_INTEGER)
    user_response = openapi.Response('Gives publications blacklist for this contractor',
                                     serializer_class)

    def get_queryset(self):
        return self.get_contractor_attribute_queryset(ContractorPublicationsList)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    @swagger_auto_schema(manual_parameters=[test_param], responses={200: user_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
