from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db.models import Model
from django.db import IntegrityError

from ...models import User, Contractor, Hashtag, NewsCharacter, NewsBurstMethod, NewsEmail, Client, NewsProject, \
    NewsWave, Currency
from crm.library.fixtures.fixtures import *


class Command(BaseCommand):
    help = "populates main_app by entities with mock data"

    def handle(self, *args, **kwargs):
        call_command('create_groups')
        call_command('add_permissions')
        self.__create_users()
        self.__create_contractors()
        self.__create_hashtags()
        self.__create_news_characters()
        self.__create_burst_methods()
        self.__create_emails()
        self.__create_clients()
        self.__create_news_projects()
        self.__create_news_waves()
        self.__create_currencies()

    def __create_users(self):

        self.__create_user_print_status(
            method=User.objects.create_superuser,
            status='Superuser',
            **(MOCK_USERS[0])
        )
        self.__create_user_print_status(
            method=User.objects.create_admin_user,
            status='Admin',
            **(MOCK_USERS[1])
        )

        self.__create_user_print_status(
            method=User.objects.create_manager_user,
            status='Manager',
            **(MOCK_USERS[2])
        )

        self.__create_user_print_status(
            method=User.objects.create_guest_user,
            status='Guest',
            **(MOCK_USERS[3])
        )

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

    def __create_currencies(self):
        self.__bulk_create_model(Currency, CURRENCIES)

    def __create_news_projects(self):
        for project in MOCK_NEWS_PROJECTS:
            project.update(
                {
                    "client": Client.objects.first(),
                    "manager": User.objects.first(),
                }
            )
        self.__bulk_create_model(NewsProject, MOCK_NEWS_PROJECTS)
        for entity in NewsProject.objects.all():
            entity.hashtags.set(Hashtag.objects.all())
            entity.contractors.set(Contractor.objects.all())
            entity.emails.set(NewsEmail.objects.all())

    def __create_news_waves(self):
        for wave in MOCK_NEWS_WAVES:
            wave.update(
                {
                    "news_character": NewsCharacter.objects.first(),
                    "burst_method": NewsBurstMethod.objects.first(),
                    "project": NewsProject.objects.first(),
                    "created_by": User.objects.first(),
                }
            )
        self.__bulk_create_model(NewsWave, MOCK_NEWS_WAVES)
        for entity in NewsWave.objects.all():
            entity.hashtags.set(Hashtag.objects.all())

    def __bulk_create_model(self, model_name: Model, mock_data: dict):
        model_name.objects.bulk_create([model_name(**element) for element in mock_data])
        self.__print_created_model(model_name.__name__)

    def __create_user_print_status(self, method, status: str = None,
                                   error_message: str = "Such a user is already created. We will skip it",
                                   **arguments) -> None:
        try:
            method(**arguments)
            self.__print_user_message(status)
        except IntegrityError:
            self.__print_user_message(error_message)
