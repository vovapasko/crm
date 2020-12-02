from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from crm.permissions.can_delete_permission import CanDeletePermission
from crm.library.constants import MESSAGE_JSON_KEY
from crm.paginations import StandardResultsSetPagination
from crm.serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from crm.models import User
from crm.views.base_view import BaseView
from crm.permissions import DjangoModelNoGetPermissions


class UsersListView(BaseView, ListCreateAPIView, UpdateAPIView):
    queryset = User.objects.all().filter(is_archived=False).order_by('id')
    permission_classes = [IsAuthenticated, CanDeletePermission, DjangoModelNoGetPermissions]
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination

    def delete(self, request: Request, pk: int) -> Response:
        try:
            user = get_object_or_404(User, pk=pk)
        except Http404:
            return self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors=dict(
                    error=f"User with id {pk} does not exist"
                )
            )

        if user.id == request.user.id:
            return self.json_forbidden_response(
                errors=dict(
                    error="You can't delete yourself!"
                )
            )

        user.delete()
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: f"User {pk} was deleted successfully"},
        )

    def put(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
