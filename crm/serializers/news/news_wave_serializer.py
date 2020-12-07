from django.db import models
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from drf_writable_nested.serializers import WritableNestedModelSerializer
from .news_project_serializer import NewsProjectSerializer
from .news_serializer import NewsSerializer
from .wave_formation_serializer import WaveFormationSerializer
from crm.models import NewsWave, Contractor, Hashtag, NewsCharacter, NewsBurstMethod
from typing import Type, List
from crm.serializers.news import NewsCharacterSerializer, NewsBurstMethodSerializer
from crm.serializers.news.news_wave_price_list_serializer import NewsWavePriceListSerializer
from crm.serializers import UserSerializer
from crm.serializers.contractors import ContractorSerializer
from crm.serializers.hashtag_serializer import HashtagSerializer


class NewsWaveSerializer(WritableNestedModelSerializer):
    news_character = NewsCharacterSerializer()
    burst_method = NewsBurstMethodSerializer()
    project = NewsProjectSerializer()
    wave_formation = WaveFormationSerializer(required=True, allow_null=True)

    hashtags = HashtagSerializer(many=True)
    news_in_project = NewsSerializer(many=True)
    created_by = UserSerializer(read_only=True)
    contractors = ContractorSerializer(many=True)

    newswavepricelist_set = NewsWavePriceListSerializer(many=True)

    class Meta:
        model = NewsWave
        fields = '__all__'
        depth = 2
        readonly = ['date_created', 'date_updated']

    def validate_newswavepricelist_set(self, my_set):
        print()
        return my_set

    def validate_news_character(self, character: str) -> str:
        self.__validate_model(character, NewsCharacter)
        return character

    def validate_project_burst_method(self, method: str) -> str:
        self.__validate_model(method, NewsBurstMethod)
        return method

    def validate_project_contractors(self, contractors: List) -> List:
        self.__validate_models_list(contractors, Contractor)
        return contractors

    def validate_project_hashtags(self, hashtags: List) -> List:
        self.__validate_models_list(hashtags, Hashtag)
        return hashtags

    def __validate_models_list(self, list: List[models.Model], model: Type[models.Model]) -> None:
        for entity in list:
            self.__validate_model(entity, model)

    def __validate_model(self, entity, model: Type[models.Model]) -> models.Model:
        id = entity.get('id')
        try:
            get_object_or_404(model, pk=id)
        except Http404:
            raise ValidationError(f"Object {model.__name__} with id {id} does not exist")

    def create(self, validated_data: dict) -> NewsWave:
        request = self.root.context.get('request')
        user = request.user
        validated_data['created_by'] = user
        return super().create(validated_data)
