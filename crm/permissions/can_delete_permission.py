from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from django.views.generic import View


class CanDeletePermission(BasePermission):
    message = {"error": "Only superuser can delete other users"}

    def has_permission(self, request: Request, view: View) -> bool:
        if request.method != 'DELETE':
            return True
        if request.method == 'DELETE' and request.user.groups.first().name == 'Superuser':
            return True
        return False
