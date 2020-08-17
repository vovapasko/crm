from crm.tests.base_test_case import BaseTestCase
from crm.models import Client, Hashtag
from django.forms.models import model_to_dict
from django.db.utils import DataError


def generate_str(*, length):
    return BaseTestCase.generate_random_string(length=length)


class ClientTestCase(BaseTestCase):
    name_max_length = Client.name_max_length
    number_max_length = Client.number_max_length
    emails_max_length = Client.emails_max_length

    VALID_CLIENT_DATA = {
        "name": generate_str(length=name_max_length),
        "numbers": generate_str(length=number_max_length),
        "emails": generate_str(length=emails_max_length),
        "price": 1,
        "amount_publications": 2,
    }
    INVALID_CLIENT_DATA_NAME = {
        "name": generate_str(length=name_max_length + 1),
        "numbers": generate_str(length=number_max_length),
        "emails": generate_str(length=emails_max_length),
        "price": 1,
        "amount_publications": 2,
    }
    INVALID_CLIENT_DATA_NUMBERS = {
        "name": generate_str(length=name_max_length),
        "numbers": generate_str(length=number_max_length + 1),
        "emails": generate_str(length=emails_max_length),
        "price": 1,
        "amount_publications": 2,
    }
    INVALID_CLIENT_DATA_EMAILS = {
        "name": generate_str(length=name_max_length),
        "numbers": generate_str(length=number_max_length),
        "emails": generate_str(length=emails_max_length + 1),
        "price": 1,
        "amount_publications": 2,
    }
    INVALID_CLIENT_DATA_PRICE = {
        "name": generate_str(length=name_max_length),
        "numbers": generate_str(length=number_max_length),
        "emails": generate_str(length=emails_max_length),
        "price": "daw",
        "amount_publications": 2,
    }
    INVALID_CLIENT_DATA_PUBLICATIONS = {
        "name": generate_str(length=name_max_length),
        "numbers": generate_str(length=number_max_length),
        "emails": generate_str(length=emails_max_length),
        "price": 1,
        "amount_publications": "dawd",
    }

    no_hashtag_keys_to_check = ['name', 'numbers', 'emails', 'price', 'amount_publications']
    with_hashtag_keys_to_check = ['name', 'numbers', 'emails', 'price', 'amount_publications', 'hashtags']

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.test_hashtag = Hashtag.objects.first()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_create_no_hashtag_client_success(self) -> None:
        client = self.__create_client(self.VALID_CLIENT_DATA)
        client.save()
        self.check_keys_in_dict(model_to_dict(client), self.no_hashtag_keys_to_check)

    def test_create_with_hasthag_client_success(self) -> None:
        client = self.__create_client(self.VALID_CLIENT_DATA)
        client.save()
        client.hashtags.add(self.test_hashtag)
        self.check_keys_in_dict(model_to_dict(client), self.with_hashtag_keys_to_check)

    def test_create_invalid_name_client(self):
        client = self.__create_client(self.INVALID_CLIENT_DATA_NAME)
        self.check_with_exception(exception=DataError, function=client.save)

    def test_create_invalid_numbers_client(self):
        client = self.__create_client(self.INVALID_CLIENT_DATA_NUMBERS)
        self.check_with_exception(exception=DataError, function=client.save)

    def test_create_invalid_emails_client(self):
        client = self.__create_client(self.INVALID_CLIENT_DATA_EMAILS)
        self.check_with_exception(exception=DataError, function=client.save)

    def test_create_invalid_price_client(self):
        client = self.__create_client(self.INVALID_CLIENT_DATA_PRICE)
        self.check_with_exception(exception=ValueError, function=client.save)

    def test_create_invalid_publications_client(self):
        client = self.__create_client(self.INVALID_CLIENT_DATA_PUBLICATIONS)
        self.check_with_exception(exception=ValueError, function=client.save)

    def __create_client(self, data: dict):
        return Client(**data)
