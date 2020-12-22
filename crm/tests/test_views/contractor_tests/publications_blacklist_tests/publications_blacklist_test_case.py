from rest_framework import status
from rest_framework.reverse import reverse

from crm.models import Contractor, ContractorPublicationsBlacklist
from crm.tests.base_test_case import BaseTestCase


class PublicationsBlacklistTestCase(BaseTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_user = cls.get_admin_user()
        cls.test_contractor = Contractor.objects.first()
        cls.post_get_url = reverse('crm:contractor-publications-blacklist', kwargs={'contractor': cls.test_contractor.id})
        cls.put_delete_url = reverse('crm:contractor-publications-blacklist', kwargs={'contractor': cls.test_contractor.id,
                                                                    'pk': str(ContractorPublicationsBlacklist.objects.last().id)})

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_publications_list_unauthorised(self):
        client = self.get_api_client(authenticated=False)
        self.__test_request_unauthorised(method=client.get)

    def test_post_publications_list_unauthorised(self):
        client = self.get_api_client(authenticated=False)
        self.__test_request_unauthorised(method=client.post)

    def test_put_publications_list_unauthorised(self):
        client = self.get_api_client(authenticated=False)
        self.__test_request_unauthorised(method=client.put)

    def test_delete_publications_list_unauthorised(self):
        client = self.get_api_client(authenticated=False)
        self.__test_request_unauthorised(method=client.delete)

    def __test_request_unauthorised(self, method):
        self._test_request_method_clients(
            method=method,
            url=self.post_get_url,
            response_code=status.HTTP_401_UNAUTHORIZED
        )

    def test_get_publications_list_authorised(self):
        client = self.get_api_client(user=self.test_user)
        response = client.get(
            path=self.post_get_url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_publications_list_authorised(self):
        client = self.get_api_client(user=self.test_user)
        self._test_request_method_clients(
            method=client.post,
            url=self.post_get_url,
            data={
                "contractor": self.test_contractor.id,
                "not_publish": "Test Edition"
            },
            response_code=status.HTTP_201_CREATED
        )

    def test_put_publications_list_authorised(self):
        client = self.get_api_client(user=self.test_user)
        self._test_request_method_clients(
            method=client.put,
            url=self.put_delete_url,
            response_code=status.HTTP_200_OK,
            data={"not_publish": "New Edition"}
        )

    def test_delete_publications_list_authorised(self):
        client = self.get_api_client(user=self.test_user)
        self._test_request_method_clients(
            method=client.delete,
            url=self.put_delete_url,
            response_code=status.HTTP_204_NO_CONTENT
        )

    def test_incorrect_post_publications_list_authorised(self):
        client = self.get_api_client(user=self.test_user)
        self._test_request_method_clients(
            method=client.post,
            url=self.post_get_url,
            data={
                "contractor": self.test_contractor,  # have to be pk, but here goes entity
                "not_publish": "Test comment"
            },
            response_code=status.HTTP_400_BAD_REQUEST
        )

