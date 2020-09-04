from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

from crm.serializers import NewsProjectSerializer
from crm.models import NewsProject
from crm.paginations import StandardResultsSetPagination
from crm.views.base_view import BaseView
from rest_framework.generics import ListCreateAPIView, DestroyAPIView, UpdateAPIView


class NewsProjectListView(BaseView, ListCreateAPIView, DestroyAPIView, UpdateAPIView):
    queryset = NewsProject.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    serializer_class = NewsProjectSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Get specified entity from queryset according to request param
        """
        queryset = NewsProject.objects.all()
        project_id = self.request.query_params.get('project', None)
        if project_id is not None:
            queryset = queryset.filter(pk=project_id)
        return queryset.order_by('id')

    def post(self, request: Request, *args, **kwargs) -> Response:
        super().post(request, *args, **kwargs)
        return Response(
            data=NewsProjectSerializer(NewsProject.objects.last()).data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)
