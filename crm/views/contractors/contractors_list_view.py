from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from ...library.constants import MESSAGE_JSON_KEY
from ...paginations import StandardResultsSetPagination
from crm.serializers import ContractorSerializer
from rest_framework import generics, permissions, status
from ...models import Contractor
from ..base_view import BaseView
from ...permissions import DjangoModelNoGetPermissions


class ContractorsListView(BaseView, generics.ListCreateAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Contractor.objects.all().order_by('id')
    permission_classes = [permissions.IsAuthenticated, DjangoModelNoGetPermissions]
    serializer_class = ContractorSerializer
    pagination_class = StandardResultsSetPagination

    def post(self, request: Request, *args, **kwargs) -> Response:
        #     """
        #     Creates new contractor
        #     body params:
        #         - editor_name: str
        #         - contact_person: str
        #         - phone_number: str
        #         - email: str (email)
        #         - news_amount: positive int
        #         - arranged_news: positive int
        #         - one_post_price: positive int
        #     :return json response
        #         http response codes:
        #             200 - ok, contractor was created successfully
        #             400 - validation error or bad request
        #             401 - bad JWT token or user unauthorized
        #         keys:
        #             response_code - response code
        #             errors - errors during validation
        #             data - all created contractor's data
        #             message - success message about successful creating
        #             contractor
        #             detail - message if user was not authorised or had bad JWT token
        #     """
        return super().post(request, *args, **kwargs)

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
        return super().delete(request, *args, **kwargs)

    def __save_contractor_send_response(self, serializer: ContractorSerializer, send_message: str) -> Response:
        serializer.save()

        return self.json_success_response(
            message={MESSAGE_JSON_KEY: send_message},
            contractor=serializer.data,
        )
