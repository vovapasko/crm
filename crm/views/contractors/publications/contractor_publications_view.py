from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.request import Request
from rest_framework.response import Response
from crm.models import ContractorPublicationsList
from crm.serializers import ContractorPublicationsListSerializer
from crm.views.contractors.contractors_attributes_base_view import ContractorAttributesBaseView


class ContractorPublicationsView(ContractorAttributesBaseView):
    serializer_class = ContractorPublicationsListSerializer
    queryset = ContractorPublicationsList.objects.all().order_by('id')

    publication_param = 'pk'
    contractor_param = ContractorAttributesBaseView.get_request_param

    publication_swagger_param = openapi.Parameter(publication_param, openapi.IN_QUERY,
                                                  description="id of publication to get",
                                                  type=openapi.TYPE_INTEGER)

    contractor_swagger_param = openapi.Parameter(contractor_param, openapi.IN_QUERY,
                                                 description="get publications list for concrete contractor",
                                                 type=openapi.TYPE_INTEGER)
    user_response = openapi.Response('Gives publications list for this contractor',
                                     serializer_class)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    @swagger_auto_schema(manual_parameters=[publication_swagger_param, contractor_swagger_param],
                         responses={200: user_response})
    def get(self, request, *args, **kwargs):
        if kwargs.get(self.publication_param):
            return super().retrieve(request, *args, **kwargs)
        return self.get_request_from_queryset(contractor=kwargs.get(self.contractor_param))
