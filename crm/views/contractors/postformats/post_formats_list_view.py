from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.generics import UpdateAPIView, ListCreateAPIView
from crm.views.base_view import BaseView
from crm.paginations import StandardResultsSetPagination
from crm.models import PostFormatList
from rest_framework.request import Request
from rest_framework.response import Response
from crm.library.constants import MESSAGE_JSON_KEY
from crm.serializers import PostFormatListSerializer


class PostFormatListView(BaseView, ListCreateAPIView, UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostFormatListSerializer
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `contractor_id` query parameter in the URL.
        """
        queryset = PostFormatList.objects.all()
        contractor_id = self.request.query_params.get('contractor', None)
        if contractor_id is not None:
            queryset = queryset.filter(contractor=contractor_id)
        return queryset.order_by('id')

    def delete(self, request: Request, pk: int) -> Response:
        try:
            postformat = get_object_or_404(PostFormatList, pk=pk)
        except Http404:
            return self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors=dict(
                    error=f"Contractor with id {pk} does not exist"
                )
            )

        postformat.delete()
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: f"PostFormatList {pk} was deleted successfully"},
        )
