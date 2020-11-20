from rest_framework import status
from rest_framework.reverse import reverse
from crm.models import Hashtag
from crm.tests.base_test_case import BaseTestCase
from .test_data import *


class HashtagTestCase(BaseTestCase):
    url = reverse('crm:hashtags')
    keys_to_check_correct_response = ['success', 'message', 'hashtag']
    keys_to_check_incorrect_response = ['success', 'message', 'errors']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        Hashtag.objects.bulk_create([Hashtag(**element) for element in hashtags])
        cls.hashtags = Hashtag.objects.all()
        cls.user = cls.get_admin_user()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_post_hashtag_unauthorised(self):
        client = self.get_api_client()
        response = client.post(
            path=self.url,
            data=correct_new_hashtag
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_hashtag_unauthorised(self):
        client = self.get_api_client()
        response = client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_hashtag(self):
        client = self.get_api_client(user=self.user)
        response = client.get(path=self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            self.get_json_content_from_response(response).get('count'),
            self.hashtags.count()
        )

    def test_post_correct_hashtag(self):
        client = self.get_api_client(user=self.user)
        response = client.post(
            path=self.url,
            data=correct_new_hashtag
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.compare_data(
            compare_what=correct_new_hashtag,
            compare_to=self.get_json_content_from_response(response).get('hashtag')
        )

    def test_empty_hashtag(self):
        self.__test_post_incorrect_hashtag(empty_hashtag)

    def test_no_field_hashtag(self):
        self.__test_post_incorrect_hashtag(no_field_hashtag)

    def test_incorrect_hashtag(self):
        self.__test_post_incorrect_hashtag(incorrect_new_hashtag)

    def __test_post_incorrect_hashtag(self, post_data):
        client = self.get_api_client(user=self.user)
        response = client.post(
            path=self.url,
            data=post_data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
