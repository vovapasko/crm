from rest_framework import permissions
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from ....library.constants import MESSAGE_JSON_KEY
from ....models import NewsWave
from ..serializers import *
from ...base_view import BaseView


class ManageNewsProjectView(BaseView, UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = NewsWave.objects.all()
    serializer_class = NewsWaveSerializer

    def get(self, request: Request, pk) -> Response:
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: f"News Project {pk} handled successfully"},
            project=self.serializer_class(NewsWave.objects.filter(pk=pk).first()).data
        )

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return self.json_success_response(
                message={MESSAGE_JSON_KEY: "News project was successfully created"},
                project=serializer.data
            )

        return self.json_failed_response(
            errors=serializer.errors
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)
