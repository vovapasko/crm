from django.core.exceptions import PermissionDenied as DjangoPermissionDenied


class ViewPermissionDenied(DjangoPermissionDenied):
    """
    Permission denied exception for better permission name saving
    """

    def __init__(self, permission_name: str, message=None) -> None:
        super().__init__(message)

        self.permission_name = permission_name
