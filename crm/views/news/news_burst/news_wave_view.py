from django.db.models import QuerySet
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.request import Request
from rest_framework.response import Response
from crm.serializers import NewsWaveSerializer
from crm.models import NewsWave
from crm.views.base_view import BaseView
from crm.serializers import NewsWaveCreateSerializer
from rest_framework import generics
from crm.paginations import StandardResultsSetPagination


class NewsWaveView(BaseView, generics.ListCreateAPIView, DestroyAPIView, UpdateAPIView):
    queryset = NewsWave.objects.all().order_by('id')
    # permission_classes = [permissions.IsAuthenticated, DjangoModelPermissions]
    serializer_class = NewsWaveSerializer
    pagination_class = StandardResultsSetPagination
    create_serializer_class = NewsWaveCreateSerializer
    # get request params
    wave_id_get_request_param = "wave"
    project_id_get_request_param = "project"

    # for swagger documentation
    project = openapi.Parameter(project_id_get_request_param, openapi.IN_QUERY,
                                description="get wave for project",
                                type=openapi.TYPE_INTEGER)
    wave = openapi.Parameter(wave_id_get_request_param, openapi.IN_QUERY,
                             description="get wave by id",
                             type=openapi.TYPE_INTEGER)

    user_response = openapi.Response('Gives wave for project or by id',
                                     serializer_class)

    @swagger_auto_schema(manual_parameters=[wave, project], responses={200: user_response})
    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        wave_id = self.request.query_params.get(self.wave_id_get_request_param, None)
        project_id = self.request.query_params.get(self.project_id_get_request_param, None)
        if wave_id is not None:
            return queryset.filter(pk=wave_id)
        if project_id is not None:
            return queryset.filter(project=project_id)
        return queryset

    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request)

    def post(self, request, *args, **kwargs) -> Response:
        serializer = self.create_serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            news_wave = serializer.save()
            try:
                self.__send_waves_via_email(news_wave)
            except Exception as e:
                print(e)
                return self.json_success_response(response_code=status.HTTP_201_CREATED,
                                                  message={'error': 'error while sending email'})
        return self.json_failed_response(data=serializer.errors)

    def __send_waves_via_email(self, news_project: NewsWave):
        pass
