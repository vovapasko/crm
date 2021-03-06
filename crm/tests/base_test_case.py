import json, string, random
from django.core import signing
from django.core.management import call_command
from django.db.models import Model
from rest_framework.test import APITestCase, APIClient
from crm.models import User
from django.forms.models import model_to_dict
from django.db.models import Model


class BaseTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.logging(f"Start testing {cls.__name__}. Initialising data")
        call_command('create_groups')
        call_command('populate')

    @classmethod
    def tearDownClass(cls):
        cls.logging(f"End testing {cls.__name__}. Erasing data")
        super().tearDownClass()

    @classmethod
    def logging(cls, message):
        print()
        print(message)

    @classmethod
    def get_test_user(cls) -> User:
        return User.objects.filter(email='admin@admin.com').first()

    @classmethod
    def get_admin_user(cls) -> User:
        return cls.get_user_by_param(email='admin@admin.com')

    @classmethod
    def get_superuser(cls) -> User:
        return cls.get_user_by_param(email='super@superuser.com')

    @classmethod
    def get_manager_user(cls) -> User:
        return cls.get_user_by_param(email='manager@manager.com')

    @classmethod
    def get_guest_user(cls) -> User:
        return cls.get_user_by_param(email='client@client.com')

    @classmethod
    def get_user_by_param(cls, **param) -> User:
        return User.objects.filter(**param).first()

    def get_api_client(self, authenticated: bool = True, user: Model = None) -> APIClient:
        """
        Returns APIClient according to parameters, which were provided
        :param authenticated: if True authenticate client with user parameter and return it
        :param user: if given, authenticates user
        :returns: APIClient instance
        """
        client = APIClient()
        if authenticated:
            client.force_authenticate(user=user)
        return client

    def compare_data(self, compare_what: dict, compare_to: dict) -> None:
        """
        Checks if compare_to dict contains keys from compare_what dict and if their values are same
        """
        for key in compare_what.keys():
            self.assertIn(member=key, container=compare_to)
            self.check_values(compare_what, compare_to, key)

    def check_keys_in_dict(self, data: dict, keys_to_check: list) -> None:
        """
        Checks if dictionary in data dict contains keys from keys_to_check list
        :param data: dict which should be checked
        :param keys_to_check: list which contains keys, which should be checked
        """
        for key in keys_to_check:
            self.assertIn(key, data)

    def check_values(self, initial_data: dict, response_data: dict, key: str) -> None:
        """
        Compares the data in initial_data and response_data according to key
        """
        self.assertEqual(initial_data.get(key), response_data.get(key))

    def check_values_many_keys(self, initial_data: dict, response_data: dict, keys: list) -> None:
        for key in keys:
            self.check_values(initial_data, response_data, key)

    def get_auth_client_and_model_last_id(self,
                                          authenticated: bool = True,
                                          user: Model = None,
                                          par_model: Model = None
                                          ) -> [APIClient, int]:
        """
        Gets client and last id of model which you test. May be useful for testing PUT request.
        """
        client = self.get_api_client(authenticated=authenticated, user=user)
        last_id = par_model.last().id
        return client, last_id

    def generate_url(self, url, key) -> str:
        return url + f"{key}"

    def get_errors_dict_from_response(self, response) -> dict:
        return self.get_json_content_from_response(response)

    def get_json_content_from_response(self, response) -> dict:
        return json.loads(response.content)

    def generate_encoded_link(self, url: str, user: User) -> str:
        data = signing.dumps(dict(id=user.id))
        return f'{url}{data}'

    def generate_random_string(chars=string.ascii_uppercase + string.digits, length=10):
        return ''.join(random.choice(chars) for _ in range(length))

    def check_with_exception(self, *, exception, function):
        with self.assertRaises(exception):
            function()

    def _test_request_method_clients(self, *, method, url, response_code, data=None):
        response = method(path=url, data=data)
        self.assertEqual(response.status_code, response_code)

    def dict_from_model(self, model: Model) -> dict:
        return model_to_dict(model)
