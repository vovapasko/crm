from crm.models import ContractorCommentList
from crm.views.base_view import BaseView
from crm.paginations import StandardResultsSetPagination
from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from crm.serializers.contractor_comment_list_serializer import ContractorCommentListSerializer
from rest_framework.request import Request
from rest_framework.response import Response


class ContractorCommentsView(BaseView, ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ContractorCommentListSerializer
    pagination_class = StandardResultsSetPagination
    get_request_param = 'contractor'

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `contractor_id` query parameter in the URL.
        """
        queryset = ContractorCommentList.objects.all()
        contractor_id = self.request.query_params.get(self.get_request_param, None)
        if contractor_id is not None:
            queryset = queryset.filter(contractor=contractor_id)
        return queryset.order_by('id')

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)
