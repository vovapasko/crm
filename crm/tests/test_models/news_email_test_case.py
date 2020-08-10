from crm.library.constants.mock_data import MOCK_EMAILS
from django.core.management import call_command
from crm.tests.base_test_case import BaseTestCase
from crm.models import NewsEmail
from django.forms.models import model_to_dict

CORRECT_EMAIL = {
    "email": "test@test.com",
    "template": "My test template",
    "signature": "My test signature",
    "codeword": "Test publisher"
}


class NewsEmailTestCase(BaseTestCase):
    keys_to_check = ['email', 'template', 'signature', 'codeword']

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.emails = NewsEmail.objects.all()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_check_elements_in_fixtures(self):
        for email in self.emails:
            self.check_keys_in_dict(model_to_dict(email), self.keys_to_check)

    def test_correct_create_new_email(self):
        new_email = NewsEmail.objects.create(**CORRECT_EMAIL)
        self.compare_data(compare_what=CORRECT_EMAIL, compare_to=model_to_dict(new_email))
