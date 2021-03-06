from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView, ListCreateAPIView, DestroyAPIView, RetrieveAPIView
from crm.permissions import DjangoModelNoGetPermissions
from crm.views.base_view import BaseView
from crm.paginations import StandardResultsSetPagination
from crm.models import PostFormatList
from rest_framework.request import Request
from rest_framework.response import Response
from crm.serializers import PostFormatListSerializer


class PostFormatListView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = PostFormatListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = PostFormatList.objects.all().order_by('id')

    contractor_param = 'contractor'
    post_format_list_param = 'pk'

    contractor_swagger_param = openapi.Parameter(contractor_param, openapi.IN_QUERY,
                                                 description="get post formats for concrete contractor",
                                                 type=openapi.TYPE_INTEGER)
    post_format_list_swagger_param = openapi.Parameter(post_format_list_param, openapi.IN_QUERY,
                                                       description='Get concrete post format',
                                                       type=openapi.TYPE_INTEGER)
    post_format_list_swagger_get_response = openapi.Response(description='Get Post Format list',
                                                             schema=serializer_class)

    @swagger_auto_schema(manual_parameters=[contractor_swagger_param, post_format_list_swagger_param],
                         responses={200: post_format_list_swagger_get_response})
    def get(self, request, *args, **kwargs):
        contractor_id = kwargs.get(self.contractor_param, None)
        postformat_id = kwargs.get(self.post_format_list_param, None)
        if contractor_id and postformat_id:
            return super().retrieve(request, *args, **kwargs)
        else:
            return self.get_request_from_queryset(contractor=contractor_id)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)

    def put(self, request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)
