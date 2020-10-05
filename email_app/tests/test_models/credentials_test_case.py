from crm.tests.base_test_case import BaseTestCase
from email_app.models import Credentials
from email_app.library.fixtures import FAKE_CREDENTIALS
from crm.models.news_email import NewsEmail


class CredentialsTestCase(BaseTestCase):
    credentials_keys_to_check = [
        'token',
        'refresh_token',
        'token_uri',
        'client_id',
        'client_secret',
        'scopes'
    ]

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_email = NewsEmail.objects.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_create_credentials(self):
        credentials = Credentials.objects.create_credentials(
            email=self.test_email.email,
            token=FAKE_CREDENTIALS['token'],
            refresh_token=FAKE_CREDENTIALS['refresh_token'],
            token_uri=FAKE_CREDENTIALS['token_uri'],
            client_id=FAKE_CREDENTIALS['client_id'],
            client_secret=FAKE_CREDENTIALS['client_secret'],
            scopes=FAKE_CREDENTIALS['scopes']
        )

        actual_cred_dict = credentials.get_credentials()
        self.check_keys_in_dict(actual_cred_dict, keys_to_check=self.credentials_keys_to_check)
