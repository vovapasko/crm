from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView, ListCreateAPIView, DestroyAPIView
from crm.permissions import DjangoModelNoGetPermissions
from crm.views.base_view import BaseView
from crm.paginations import StandardResultsSetPagination
from crm.models import PostFormatList
from rest_framework.request import Request
from rest_framework.response import Response
from crm.library.constants import MESSAGE_JSON_KEY
from crm.serializers import PostFormatListSerializer


class PostFormatListView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = PostFormatListSerializer
    pagination_class = StandardResultsSetPagination
    queryset = PostFormatList.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        contractor_id = kwargs.get('contractor', None)
        if contractor_id:
            queryset = self.queryset.filter(contractor=contractor_id)
            return self.make_response(
                data=self.serializer_class(
                    instance=queryset, many=True
                ).data
            )
        return super(PostFormatListView, self).get(request, *args, **kwargs)

    def delete(self, request: Request, *args, **kwargs) -> Response:
        return super().delete(request, *args, **kwargs)
