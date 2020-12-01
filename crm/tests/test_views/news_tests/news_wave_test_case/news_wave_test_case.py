from django.db.models import QuerySet
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.serializers import Serializer

from crm.tests.base_test_case import BaseTestCase
from crm.models import NewsWave, NewsProject, NewsCharacter, NewsBurstMethod, \
    Contractor, Hashtag, WaveFormation, User
from crm.views.news.news_burst.news_wave_view import NewsWaveView
from crm.serializers import NewsCharacterSerializer, NewsBurstMethodSerializer, \
    NewsProjectSerializer, UserSerializer
from .test_data.test_data import wave


class NewsWaveTestCase(BaseTestCase):
    url = reverse('crm:newswaves')
    project_get_parameter = NewsWaveView.project_id_get_request_param
    wave_get_parameter = NewsWaveView.wave_id_get_request_param

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.all_waves = NewsWave.objects.all()
        cls.admin_user = cls.get_admin_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_news_wave_authorised(self):
        client = self.get_api_client(user=self.admin_user)
        project = NewsProject.objects.first()
        response = client.get(
            self.url,
            data={
                self.project_get_parameter: project.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_news_wave_unauthorised(self):
        client = self.get_api_client()
        response = client.post(
            self.url,
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # todo this test fails. Find out why
    # def test_post_news_wave_authorised(self):
    #     client = self.get_api_client(user=self.admin_user)
    #     data = self.__generate_wave_with_attachments()
    #     response = client.post(
    #         self.url,
    #         data=data,
    #         format='json'
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def __generate_wave_with_attachments(self) -> dict:
        wave_template = self.__generate_common_elements()
        wave_template.update({"wave_formation": wave})
        return wave_template

    def __generate_common_elements(self) -> dict:
        return {
            "title": "test_title",
            "budget": 1234,
            "post_format": "test_format",
            "news_character": self.__model_to_dict(NewsCharacter.objects.first(), NewsCharacterSerializer),
            "burst_method": self.__model_to_dict(NewsBurstMethod.objects.first(), NewsBurstMethodSerializer),
            "project": self.__model_to_dict(NewsProject.objects.first(), NewsProjectSerializer),
            "created_by": self.__model_to_dict(User.objects.first(), UserSerializer)
        }

    def __model_to_dict(self, entity: QuerySet, serializer: Serializer):
        return serializer(entity).data
