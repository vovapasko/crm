from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Model

from ...models import User, Contractor, Hashtag, NewsCharacter, NewsBurstMethod, NewsEmail, Client
from ...library.constants.mock_data import *


class Command(BaseCommand):
    help = "populates main_app by entities with mock data"

    def handle(self, *args, **kwargs):
        call_command('upgrade_groups')
        self.__create_users()
        self.__create_contractors()
        self.__create_hashtags()
        self.__create_news_characters()
        self.__create_burst_methods()
        self.__create_emails()
        self.__create_clients()

    def __create_users(self):
        User.objects.create_superuser(
            email=TEST_SUPERUSER_EMAIL,
            password=TEST_SUPERUSER_PASSWORD
        )
        self.__print_user_message("Superuser")

        User.objects.create_admin_user(
            email=TEST_ADMIN_EMAIL,
            password=TEST_ADMIN_PASSWORD
        )
        self.__print_user_message("Admin")

        User.objects.create_manager_user(
            email=TEST_MANAGER_EMAIL,
            password=TEST_MANAGER_PASSWORD
        )
        self.__print_user_message("Manager")

        User.objects.create_client_user(
            email=TEST_CLIENT_EMAIL,
            password=TEST_CLIENT_PASSWORD
        )
        self.__print_user_message("Client")

    def __create_contractors(self):
        for mock_data in MOCK_CONTRACTORS_DATA:
            Contractor.objects.create_contractor(**mock_data)
        self.stdout.write("Created mock contractors")

    def __print_user_message(self, user_role: str):
        self.stdout.write(f'Created {user_role} mock user')

    def __print_created_model(self, model_name: str):
        self.stdout.write(f'Created {model_name} model samples')

    def __create_hashtags(self):
        self.__bulk_create_model(Hashtag, HASHTAGS)

    def __create_news_characters(self):
        self.__bulk_create_model(NewsCharacter, NEWS_CHARACTER)

    def __create_burst_methods(self):
        self.__bulk_create_model(NewsBurstMethod, BURST_METHODS)

    def __create_emails(self):
        self.__bulk_create_model(NewsEmail, MOCK_EMAILS)

    def __create_clients(self):
        self.__bulk_create_model(Client, MOCK_CLIENTS)

    def __bulk_create_model(self, model_name: Model, mock_data: dict):
        model_name.objects.bulk_create([model_name(**element) for element in mock_data])
        self.__print_created_model(model_name.__name__)
