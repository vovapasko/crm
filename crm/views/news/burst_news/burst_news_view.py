import json

from django.db.models import QuerySet
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from crm.serializers import ContractorSerializer
from crm.library.constants import MESSAGE_JSON_KEY
from crm.views.base_view import BaseView
from crm.models import Contractor, Hashtag, NewsCharacter, NewsBurstMethod, PostFormatList
from crm.serializers import HashtagSerializer, NewsBurstMethodSerializer, NewsCharacterSerializer
from typing import List
from crm.permissions import DjangoModelNoGetPermissions


# todo i should come back here
class BurstNewsView(BaseView):
    permission_classes = [permissions.IsAuthenticated]

    contractor_serializer = ContractorSerializer
    hashtag_serializer = HashtagSerializer
    burst_method_serializer = NewsBurstMethodSerializer
    character_serializer = NewsCharacterSerializer

    def get(self, request: Request) -> Response:
        return self.json_success_response(
            message={MESSAGE_JSON_KEY: "Data handled successfully"},
            contractors=self.__get_objects_with_filter(self.contractor_serializer, Contractor),
            hashtags=self.__get_objects_with_filter(self.hashtag_serializer, Hashtag),
            characters=self.__get_objects(self.character_serializer, NewsCharacter),
            burst_methods=self.__get_objects(self.burst_method_serializer, NewsBurstMethod),
            formats=self.__to_json(
                PostFormatList.objects.all().values('post_format').distinct()
            )
        )

    def __get_objects(self, serializer: Serializer, obj_class: object) -> List:
        return serializer(obj_class.objects.all(), many=True).data

    def __get_objects_with_filter(self, serializer: Serializer, obj_class: object) -> List:
        return serializer(obj_class.objects.all().filter(is_archived=False), many=True).data

    def __to_json(self, queryset: QuerySet) -> list:
        return json.loads(json.dumps(list(queryset)))
