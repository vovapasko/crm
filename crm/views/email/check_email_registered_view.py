from ..base_view import BaseView
from ...models import User
from django.shortcuts import get_object_or_404
from django.http import Http404
from rest_framework import status
from ...library.constants import MESSAGE_JSON_KEY
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.request import Request


# checks if email is registered in system
class CheckEmailRegisteredView(BaseView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, email: str, *args, **kwargs) -> Response:
        try:
            user = get_object_or_404(User, email=email)
        except Http404:
            return self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors=dict(
                    error=f"User with mail {email} is not found"
                ),
            )

        return self.json_success_response(
            message={
                MESSAGE_JSON_KEY: f"User with {email} is registered"
            }
        )
