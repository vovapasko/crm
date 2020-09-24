from crm.views.base_view import BaseView
from rest_framework.request import Request
from rest_framework.response import Response


class GmailCredentialsClearView(BaseView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.make_response(data={"Message": "Credentials cleared"})
