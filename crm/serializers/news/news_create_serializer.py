from .news_serializer import NewsSerializer
from .news_attachment_put_serializer import NewsAttachmentPutSerializer


class NewsCreateSerializer(NewsSerializer):
    attachments = NewsAttachmentPutSerializer(many=True, required=False)
