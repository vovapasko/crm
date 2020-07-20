from rest_framework import permissions
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView

from ..serializers.news_email_serializer import NewsEmailSerializer
from ....models import NewsEmail
from ....paginations import StandardResultsSetPagination
from ....views import BaseView


class NewsEmailListView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = NewsEmail.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewsEmailSerializer
    pagination_class = StandardResultsSetPagination
