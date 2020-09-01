from crm.tests.base_test_case import BaseTestCase
from crm.models import Contractor, Hashtag, NewsEmail, Client, NewsProject
from django.forms.models import model_to_dict


class NewsProjectTestCase(BaseTestCase):
    keys_to_check = ['name', 'budget', 'client', 'manager', 'hashtags', 'contractors', 'emails']
    CORRECT_INIT_PROJECT_DATA = {
        "name": "My project",
        "budget": 1234,
    }

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_manager = cls.get_admin_user()
        cls.test_contractor = Contractor.objects.first()
        cls.test_hashtag = Hashtag.objects.first()
        cls.test_email = NewsEmail.objects.first()
        cls.test_client = Client.objects.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_correct_news_project_create(self):
        correct_project_data = self.CORRECT_INIT_PROJECT_DATA.update(
            {
                "client": self.test_client,
                "manager": self.test_manager
            }
        )
        news_project = NewsProject(
            correct_project_data
        )
        news_project.save()
        news_project.hashtags.add(self.test_hashtag)
        news_project.contractors.add(self.test_contractor)
        news_project.emails.add(self.test_email)
        self.check_keys_in_dict(model_to_dict(news_project), self.keys_to_check)
