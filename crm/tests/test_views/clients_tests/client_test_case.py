from crm.tests.base_test_case import BaseTestCase
from rest_framework.reverse import reverse
from rest_framework import status
from crm.models import Client, Hashtag


class ClientTestCase(BaseTestCase):
    url = reverse('crm:clients')
    CORRECT_CLIENT_DATA = {
        "name": "John",
        "numbers": "+380501112233",
        "emails": "john@client.com",
        "price": 8400,
        "amount_publications": 150
    }
    put_data = {"name": "corrected name"}

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_admin_user = cls.get_admin_user()
        cls.client = Client.objects.first()
        cls.put_delete_url = f"{cls.url}{cls.client.id}"
        cls.hashtag = Hashtag.objects.first()
        cls.correct_post_data = cls.CORRECT_CLIENT_DATA.update({'hashtags': cls.hashtag})

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_clients_unauthenticated(self):
        client = self.get_api_client()
        self.__test_request_method_clients(
            method=client.get,
            url=self.url,
            response_code=status.HTTP_401_UNAUTHORIZED
        )

    def test_post_clients_unauthenticated(self):
        client = self.get_api_client()
        self.__test_request_method_clients(
            method=client.post,
            url=self.url,
            data=self.correct_post_data,
            response_code=status.HTTP_401_UNAUTHORIZED
        )

    def test_put_clients_unauthenticated(self):
        client = self.get_api_client()
        self.__test_request_method_clients(
            method=client.put,
            url=self.put_delete_url,
            data=self.put_data,
            response_code=status.HTTP_401_UNAUTHORIZED
        )

    def test_delete_clients_unauthenticated(self):
        client = self.get_api_client()
        self.__test_request_method_clients(
            method=client.delete,
            url=self.put_delete_url,
            response_code=status.HTTP_401_UNAUTHORIZED
        )

    def test_get_clients_authenticated(self):
        client = self.get_api_client(user=self.test_admin_user)
        self.__test_request_method_clients(
            method=client.get,
            url=self.url,
            response_code=status.HTTP_200_OK
        )

    def test_post_no_hashtags_clients_authenticated(self):
        client = self.get_api_client(user=self.test_admin_user)
        self.__test_request_method_clients(
            method=client.post,
            url=self.url,
            data=self.CORRECT_CLIENT_DATA,
            response_code=status.HTTP_400_BAD_REQUEST
        )

    def test_post_with_clients_authenticated(self):
        client = self.get_api_client(user=self.test_admin_user)
        self.__test_request_method_clients(
            method=client.post,
            url=self.url,
            data=self.correct_post_data,
            response_code=status.HTTP_400_BAD_REQUEST
        )

    def test_put_clients_authenticated(self):
        client = self.get_api_client(user=self.test_admin_user)
        self.__test_request_method_clients(
            method=client.put,
            url=self.put_delete_url,
            response_code=status.HTTP_200_OK,
            data=self.put_data
        )

    def test_delete_clients_authenticated(self):
        client = self.get_api_client(user=self.test_admin_user)
        self.__test_request_method_clients(
            method=client.delete,
            url=self.put_delete_url,
            response_code=status.HTTP_204_NO_CONTENT
        )

    def __test_request_method_clients(self, *, method, url, response_code, data=None):
        response = method(path=url, data=data)
        self.assertEqual(response.status_code, response_code)
