from drf_yasg.utils import swagger_auto_schema
from crm.models import ContractorCommentList
from crm.serializers.contractors.contractor_comment_list_serializer import ContractorCommentListSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from drf_yasg import openapi
from crm.views.contractors.contractors_attributes_base_view import ContractorAttributesBaseView


class ContractorCommentsView(ContractorAttributesBaseView):
    serializer_class = ContractorCommentListSerializer
    queryset = ContractorCommentList.objects.all().order_by('id')

    comment_param = 'pk'
    contractor_param = ContractorAttributesBaseView.get_request_param

    comment_swagger_param = openapi.Parameter(comment_param, openapi.IN_QUERY,
                                              description="id of comment to get",
                                              type=openapi.TYPE_INTEGER)

    contractor_swagger_param = openapi.Parameter(ContractorAttributesBaseView.get_request_param, openapi.IN_QUERY,
                                                 description="get comments for concrete contractor",
                                                 type=openapi.TYPE_INTEGER)
    user_response = openapi.Response('Gives comments for this contractor or concrete comment',
                                     serializer_class)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    @swagger_auto_schema(manual_parameters=[comment_swagger_param, contractor_swagger_param],
                         responses={200: user_response})
    def get(self, request, *args, **kwargs):
        if kwargs.get(self.comment_param):
            return super().retrieve(request, *args, **kwargs)
        return self.get_request_from_queryset(contractor=kwargs.get(self.contractor_param))
