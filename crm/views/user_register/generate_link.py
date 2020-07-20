from ..base_view import BaseView
from django.http import HttpResponse
from ...library.constants import HTTP_HOST, USER_CONFIRM_API
from django.core import signing
from rest_framework.request import Request


class GenerateLinkView(BaseView):
    def get(self, request: Request, *args, **kwargs) -> HttpResponse:
        data = signing.dumps(dict(id=1))
        link = f'{request.META[HTTP_HOST]}/{USER_CONFIRM_API.split(":")[1]}/{data}'
        return HttpResponse(link)
