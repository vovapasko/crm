from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi
from crm.models import ContractorPublicationsBlacklist
from crm.serializers.contractors.contractor_publications_blacklist_serializer import \
    ContractorPublicationsBlacklistSerializer
from crm.views.contractors.contractors_attributes_base_view import ContractorAttributesBaseView


class ContractorPublicationsBlacklistView(ContractorAttributesBaseView):
    serializer_class = ContractorPublicationsBlacklistSerializer
    queryset = ContractorPublicationsBlacklist.objects.all().order_by('id')

    contractor_param = ContractorAttributesBaseView.get_request_param
    blacklist_param = 'pk'

    contractor_swagger_param = openapi.Parameter(contractor_param, openapi.IN_QUERY,
                                                 description="get publications blacklist for concrete contractor",
                                                 type=openapi.TYPE_INTEGER)
    blacklist_swagger_param = openapi.Parameter(blacklist_param, openapi.IN_QUERY,
                                                description='get concrete publications blacklist',
                                                type=openapi.TYPE_INTEGER)

    user_response = openapi.Response('Gives publications blacklist for this contractor',
                                     ContractorPublicationsBlacklistSerializer)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    @swagger_auto_schema(manual_parameters=[contractor_swagger_param, blacklist_swagger_param],
                         responses={200: user_response})
    def get(self, request, *args, **kwargs):
        return super().get_contractor_entity_response(request, key=self.blacklist_param, *args, **kwargs)
