from drf_yasg.utils import swagger_auto_schema
from crm.models import ContractorCommentList
from crm.serializers.contractors.contractor_comment_list_serializer import ContractorCommentListSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi

from crm.views.contractors.contractors_attributes_base_view import ContractorAttributesBaseView


class ContractorCommentsView(ContractorAttributesBaseView):
    serializer_class = ContractorCommentListSerializer

    test_param = openapi.Parameter(ContractorAttributesBaseView.get_request_param, openapi.IN_QUERY,
                                   description="get comments for concrete contractor",
                                   type=openapi.TYPE_INTEGER)
    user_response = openapi.Response('Gives comments for this contractor',
                                     serializer_class)

    def get_queryset(self):
        return self.get_contractor_attribute_queryset(ContractorCommentList)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    @swagger_auto_schema(manual_parameters=[test_param], responses={200: user_response})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
