from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from crm.views.base_view import BaseView
from rest_framework import generics
from crm.models import Hashtag
from crm.serializers import HashtagSerializer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from crm.library.constants import MESSAGE_JSON_KEY
from crm.paginations import StandardResultsSetPagination


class HashtagsListView(BaseView, generics.ListCreateAPIView, DestroyAPIView):
    queryset = Hashtag.objects.all().order_by('id')
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = HashtagSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        body params:
            name: [str] the name of the new hashtag
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return self.save_hashtag_and_response(serializer)

        return self.json_failed_response(
            message=dict(
                message="Creating hashtag failed"
            ),
            errors=serializer.errors
        )

    def save_hashtag_and_response(self, serializer: Serializer) -> Response:
        serializer.save()

        return self.json_success_response(
            message={MESSAGE_JSON_KEY: "Hashtag created successfully"},
            hashtag=serializer.data
        )
