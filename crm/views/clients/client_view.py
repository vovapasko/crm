from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from crm.paginations import StandardResultsSetPagination
from crm.permissions import DjangoModelNoGetPermissions
from crm.views import BaseView
from crm.models import Client
from crm.serializers import ClientSerializer


class ClientView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Client.objects.all().filter(is_archived=False).order_by('id')
    permission_classes = [IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = ClientSerializer
    pagination_class = StandardResultsSetPagination

    def put(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request)
