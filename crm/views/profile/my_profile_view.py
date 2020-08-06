from rest_framework.generics import UpdateAPIView
from .can_change_permission import CanChangePermission
from crm.serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from crm.views.base_view import BaseView
from crm.models import User
from crm.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.request import Request


class MyProfileView(BaseView, UpdateAPIView):
    permission_classes = [IsAuthenticated, CanChangePermission]
    serializer_class = ProfileSerializer
    user_serializer = UserSerializer
    queryset = User.objects.all()

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        request params:
            - first_name
            - last_name
            - avatar
        :return json response
            http response codes:
                200 - ok, profile updated successfully
                400 - validation failed
                401 - if user is unauthorized or has invalid token
                403 - user has not the permission to change profile of other users
        """
        return self.partial_update(request)
