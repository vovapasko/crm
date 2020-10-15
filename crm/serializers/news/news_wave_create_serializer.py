from .news_create_serializer import NewsCreateSerializer
from .news_wave_serializer import NewsWaveSerializer


class NewsWaveCreateSerializer(NewsWaveSerializer):
    news_in_project = NewsCreateSerializer()
