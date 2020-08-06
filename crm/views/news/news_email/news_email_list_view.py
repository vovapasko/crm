from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from crm.serializers.news.news_email_serializer import NewsEmailSerializer
from crm.models import NewsEmail
from crm.paginations import StandardResultsSetPagination
from crm.views.base_view import BaseView


class NewsEmailListView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = NewsEmail.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewsEmailSerializer
    pagination_class = StandardResultsSetPagination
