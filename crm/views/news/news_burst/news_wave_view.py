from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.generics import DestroyAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from crm.serializers import NewsWaveSerializer
from crm.models import NewsWave
from crm.views.base_view import BaseView
from rest_framework import generics
from crm.paginations import StandardResultsSetPagination


class NewsWaveView(BaseView, generics.ListCreateAPIView, DestroyAPIView, UpdateAPIView):
    queryset = NewsWave.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewsWaveSerializer
    pagination_class = StandardResultsSetPagination

    # get request param
    get_request_wave_param = "wave"

    def get(self, request: Request, *args, **kwargs) -> Response:
        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        """
        Get specified entity from queryset according to request param
        """
        queryset = NewsWave.objects.all()
        wave_id = self.request.query_params.get(self.get_request_wave_param, None)
        if wave_id is not None:
            queryset = queryset.filter(pk=wave_id)
        return queryset.order_by('id')

    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request)
