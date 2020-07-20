from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from .can_delete_permission import CanDeletePermission
from ...library.constants import MESSAGE_JSON_KEY
from ...paginations import StandardResultsSetPagination
from ...serializers import UserSerializer
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from ...models import User
from ..base_view import BaseView


class UsersListView(BaseView, ListCreateAPIView):
    queryset = User.objects.all().order_by('id')
    permission_classes = [IsAuthenticated, CanDeletePermission]
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
