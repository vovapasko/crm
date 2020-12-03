from crm.models import Contractor, User
from rest_framework.test import APIClient
from rest_framework import status

from .test_data import *
from crm.tests.base_test_case import BaseTestCase


class ContractorTestCase(BaseTestCase):
    url = "/contractors/"
    error_check_key = "detail"

    @classmethod
    def setUpTestData(cls: object) -> None:
        super().setUpTestData()
        cls.admin_user = super().get_test_user()
        cls.superuser = super().get_superuser()
        cls.contractors = Contractor.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_contractors_authorised(self) -> None:
        client = self.get_api_client(user=self.admin_user)
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.check_keys_in_dict(response.data, keys_to_check)
        # next line compares amount of entities in request and in database
        self.assertEqual(response.data.get('count'), self.contractors.count())

    def test_get_contractors_unathorised(self) -> None:
        client = APIClient()
        response = client.get(self.url, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_contractors_authorised(self) -> None:
        client = self.get_api_client(user=self.admin_user)
        response = client.post(self.url, data=mock_contractor, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.compare_data(mock_contractor, self.get_json_content_from_response(response).get('contractor'))

    def test_post_contractors_unauthorised(self) -> None:
        client = APIClient()
        response = client.post(self.url, data=mock_contractor, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_correct_contractors_authorised(self) -> None:
        client, last_id = self.get_auth_client_and_model_last_id(user=self.admin_user, par_model=self.contractors)
        response = client.put(
            path=self.generate_url(self.url, last_id),
            data=correct_put_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.compare_data(correct_put_data, self.get_json_content_from_response(response))

    # todo add testing wrong values i.e more than int range numbers
    # def test_put_wrong_contractors_authorised(self) -> None:
    #     client, last_id = self.get_auth_client_and_model_last_id(user=self.user, par_model=self.contractors)
    #     wrong_minus_data_response = client.put(
    #         path=self.generate_url(self.url, last_id),
    #         data=wrong_put_data_minus_number,
    #         format='json'
    #     )
    #     wrong_nan_response = client.put(
    #         path=self.generate_url(self.url, last_id),
    #         data=wrong_put_data_nan,
    #         format='json'
    #     )
    #     self.assertEqual(wrong_minus_data_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(wrong_nan_response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.check_response_data_keys(
    #         self.get_json_content_from_response(wrong_minus_data_response),
    #         wrong_put_data_minus_number.keys()
    #     )
    #     self.check_response_data_keys(
    #         self.get_json_content_from_response(wrong_nan_response),
    #         wrong_put_data_nan.keys()
    #     )

    def test_put_contractors_unauthorised(self) -> None:
        client, last_id = self.get_auth_client_and_model_last_id(
            authenticated=False,
            user=self.admin_user,
            par_model=self.contractors
        )
        response = client.put(
            path=self.generate_url(self.url, last_id),
            data=mock_contractor,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn(member=self.error_check_key, container=self.get_json_content_from_response(response))

    def test_delete_contractors_admin_authorised(self) -> None:
        self.__delete_contractor_by_user(user=self.admin_user, expected_status_code=status.HTTP_403_FORBIDDEN)

    def test_delete_contractors_superuser_authorised(self):
        last_id = self.__delete_contractor_by_user(user=self.superuser, expected_status_code=status.HTTP_204_NO_CONTENT)
        self.__delete_contractor_by_user(
            user=self.superuser,
            expected_status_code=status.HTTP_404_NOT_FOUND,
            last_id_param=last_id
        )

    def __delete_contractor_by_user(self, user: User, expected_status_code: int, last_id_param=None) -> None:
        client, last_id = self.get_auth_client_and_model_last_id(
            user=user,
            par_model=self.contractors
        )
        if last_id_param:
            last_id = last_id_param
        response = client.delete(
            path=self.generate_url(self.url, last_id)
        )
        # admin is forbidden can not delete contractor
        self.assertEqual(response.status_code, expected_status_code)
        return last_id
