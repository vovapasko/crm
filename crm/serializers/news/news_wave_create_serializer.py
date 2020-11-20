from .news_create_serializer import NewsCreateSerializer
from .news_wave_serializer import NewsWaveSerializer
from .wave_formation_create_serializer import WaveFormationCreateSerializer


class NewsWaveCreateSerializer(NewsWaveSerializer):
    news_in_project = NewsCreateSerializer(many=True)
    wave_formation = WaveFormationCreateSerializer(required=True, allow_null=True)
