from crm.views.base_view import BaseView
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated


class ContractorPublicationsView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    