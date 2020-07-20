from rest_framework import viewsets, status, permissions
from rest_framework.generics import ListAPIView, DestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.request import Request
from rest_framework.response import Response

from ... import BaseView
from ....models import NewsAttachment
from ..serializers import NewsAttachmentSerializer, NewsAttachmentPutSerializer


class NewsFileUploadView(BaseView, DestroyAPIView, ListAPIView):
    parser_classes = [MultiPartParser, FormParser]
    queryset = NewsAttachment.objects.all().order_by('id')
    serializer_class = NewsAttachmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request: Request) -> Response:
        serializer = NewsAttachmentPutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return self.json_failed_response(errors=serializer.errors)
