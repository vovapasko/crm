from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from crm.serializers.news.news_email_serializer import NewsEmailSerializer
from crm.models import NewsEmail
from crm.paginations import StandardResultsSetPagination
from crm.views.base_view import BaseView
from crm.permissions import DjangoModelNoGetPermissions


class NewsEmailListView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = NewsEmail.objects.all().filter(is_archived=False).order_by('id')
    permission_classes = [permissions.IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = NewsEmailSerializer
    pagination_class = StandardResultsSetPagination

    def put(self, request, *args, **kwargs):
        return super().partial_update(request)
