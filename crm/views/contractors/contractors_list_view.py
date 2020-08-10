from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from ...library.constants import MESSAGE_JSON_KEY
from ...paginations import StandardResultsSetPagination
from crm.serializers import ContractorSerializer
from rest_framework import generics, permissions, status
from ...models import Contractor
from ..base_view import BaseView


class ContractorsListView(BaseView, generics.ListCreateAPIView, UpdateAPIView):
    queryset = Contractor.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ContractorSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        Creates new contractor
        body params:
            - editor_name: str
            - contact_person: str
            - phone_number: str
            - email: str (email)
            - news_amount: positive int
            - arranged_news: positive int
            - one_post_price: positive int
        :return json response
            http response codes:
                200 - ok, contractor was created successfully
                400 - validation error or bad request
                401 - bad JWT token or user unauthorized
            keys:
                response_code - response code
                errors - errors during validation
                data - all created contractor's data
                message - success message about successful creating
                contractor
                detail - message if user was not authorised or had bad JWT token
        """
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            return self.__save_contractor_send_response(
                serializer,
                f"Created contractor",
            )

        return self.json_failed_response(errors=serializer.errors)

    def put(self, request: Request, *args, **kwargs) -> Response:
        return self.partial_update(request)

    def delete(self, request: Request, pk: int, *args, **kwargs) -> Response:
        """
        Deletes contractor
        request params:
            - pk: int - primary key of contractor
        :return json response
            http response codes:
                204 - ok, entity was deleted successfully
                404 - contractor you try to delete does not exits
            keys:
                response_code - response code
                errors - errors during validation
                message - success message about successful deleting contractor
        """
        try:
            contractor = get_object_or_404(Contractor, pk=pk)
        except Http404:
            return self.json_failed_response(
                response_code=status.HTTP_404_NOT_FOUND,
                errors=dict(
                    error=f"Contractor with id {pk} does not exist"
                )
            )

        contractor.delete()
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: f"Contractor {pk} was deleted successfully"},
        )

    def __save_contractor_send_response(self, serializer: ContractorSerializer, send_message: str) -> Response:
        serializer.save()

        return self.json_success_response(
            message={MESSAGE_JSON_KEY: send_message},
            contractor=serializer.data,
        )
