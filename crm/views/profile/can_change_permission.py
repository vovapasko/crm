from rest_framework.permissions import BasePermission


class CanChangePermission(BasePermission):
    """
    This permission controls that user can change data only in his profile
    """
    message = {"error": "You can change only your profile"}

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user
