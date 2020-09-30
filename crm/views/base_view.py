from django.db.models import Model, QuerySet
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication as jwt_auth
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework_simplejwt.exceptions import InvalidToken
from crm.library.constants import *
from crm.library.exceptions import ViewPermissionDenied
from crm.library.helpers import get_name_from_permission
from crm.models import User
from rest_framework.request import Request
from typing import Type, Union


class BaseView(APIView):

    def make_response(self, data, **kwargs):
        return Response(data=data, **kwargs)

    def json_response(self, response_code: int, **kwargs):
        return Response(kwargs, status=response_code)

    def json_success_response(self, response_code: int = status.HTTP_200_OK, message: dict = None,
                              **kwargs) -> Response:
        return self.json_response(
            response_code=response_code,
            success=True,
            message=message,
            **kwargs
        )

    def json_failed_response(self, response_code: int = status.HTTP_400_BAD_REQUEST, errors: dict = None,
                             **kwargs) -> Response:
        return self.json_response(
            response_code=response_code,
            success=False,
            errors=errors,
            **kwargs
        )

    def json_forbidden_response(self, response_code: int = status.HTTP_403_FORBIDDEN, errors: dict = None,
                                **kwargs) -> Response:
        return self.json_failed_response(
            response_code=response_code,
            errors=errors,
            **kwargs
        )

    def get_user_object(self, pk: int) -> User:
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def send_error_message(self, status: int, errors: str) -> Response:
        return self.json_response(
            status=status,
            errors=errors
        )

    def dispatch(self, request: Request, *args, **kwargs):
        """
        overriding for django permissions check
        """
        return self.__check_permissions_from_jwt(request) or super().dispatch(request, *args, **kwargs)

    def __check_permissions_from_jwt(self, request: Request):
        """
        get user from jwt and check it's permissions if necessary
        :return: Response if has problems (no jwt, invalid jwt, no permission)
                 None if all is ok
        """
        try:
            user = self.__get_user_from_request(request)
        except InvalidToken as e:
            return self.__create_response_object(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message={'error': e.default_code}
            )

        if user is not None and getattr(user, 'is_confirmed') is False:
            return self.__create_response_object(
                status_code=status.HTTP_403_FORBIDDEN,
                message={'message': 'user is not confirmed'}
            )

        if user is not None and hasattr(self, 'permission_required'):
            try:
                self.__check_user_permissions(user)
            except ViewPermissionDenied as e:
                return self.__create_response_object(
                    status_code=status.HTTP_403_FORBIDDEN,
                    message={'permission_required': e.permission_name}
                )

    def __check_user_permissions(self, user: User):
        """
        check all permissions from permission_required of view
        :param user: User object
        :raise PermissionDenied exception
        """
        for permission in self.permission_required:
            if not user.has_perm(permission):
                raise ViewPermissionDenied(
                    get_name_from_permission(permission))

    def __get_user_from_request(self, request: Request):
        """
        try to get user form jwt in request, return None if no jwt
        :return: User object
        """
        token = jwt_auth().authenticate(request)

        if token is not None:
            user_id = token[1].payload[USER_ID]
            return User.objects.get(pk=user_id)

        return None

    def __create_response_object(self, status_code: int, message: dict = None) -> Response:
        """
        create response object to return
        :param message: permission name for response
        :return: response object
        """
        response = Response(status=status_code)

        response.accepted_renderer = JSONRenderer()
        response.accepted_media_type = "application/json"
        response.renderer_context = {}

        response.data = message

        return response

    def get_entity_or_json_error(self, model: Type[Model], pk: int):
        entity, error_json = None, None
        try:
            entity = get_object_or_404(model, pk=pk)
        except Http404:
            error_json = self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors=dict(
                    error=f"{model.__name__} with id {pk} does not exist"
                )
            )
        return entity, error_json

    def get_custom_queryset(self, *, model: Type[Model], query_param: Union[str, int],
                            order_by_param: str = 'id') -> QuerySet:
        """
                Get specified entity from queryset according to request param
                """
        queryset = model.objects.all()
        entity = self.request.query_params.get(query_param, None)
        if entity is not None:
            queryset = queryset.filter(query_param=entity)
        return queryset.order_by(order_by_param)
