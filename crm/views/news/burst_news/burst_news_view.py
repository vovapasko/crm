import json

from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from ... import ContractorSerializer
from ....library.constants import MESSAGE_JSON_KEY
from ....views import BaseView
from ....models import Contractor, Hashtag, NewsCharacter, NewsBurstMethod, PostFormatList
from ..serializers import *
from typing import List


class BurstNewsView(BaseView):
    permission_classes = [permissions.IsAuthenticated]

    contractor_serializer = ContractorSerializer
    hashtag_serializer = HashtagSerializer
    burst_method_serializer = NewsBurstMethodSerializer
    character_serializer = NewsCharacterSerializer

    def get(self, request: Request) -> Response:
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: "Data handled successfully"},
            contractors=self.__get_objects(self.contractor_serializer, Contractor),
            hashtags=self.__get_objects(self.hashtag_serializer, Hashtag),
            characters=self.__get_objects(self.character_serializer, NewsCharacter),
            burst_methods=self.__get_objects(self.burst_method_serializer, NewsBurstMethod),
            formats=self.__to_json(
                PostFormatList.objects.all().values('post_format').distinct()
            )
        )

    def __get_objects(self, serializer: Serializer, obj_class: object) -> List:
        return serializer(obj_class.objects.all(), many=True).data

    def __to_json(self, queryset: QuerySet) -> list:
        return json.loads(json.dumps(list(queryset)))
