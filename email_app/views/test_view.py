from crm.views.base_view import BaseView
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated


class TestView(BaseView, ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.json_success_response(message={"message": "Good get"})

    def post(self, request, *args, **kwargs):
        return self.json_success_response(message={"message": "Good post"})
