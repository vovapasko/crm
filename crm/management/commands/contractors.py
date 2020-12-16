from django.core.management import BaseCommand
from crm.library.fixtures.fixtures import *
from crm.models import Contractor


class Command(BaseCommand):
    help = "populates main_app by entities with mock data"

    def handle(self, *args, **kwargs):
        contractor_amounts = 200
        contractors = [MOCK_CONTRACTORS_DATA[0]] * contractor_amounts
        Contractor.objects.bulk_create([Contractor(**contractor) for contractor in contractors])
        self.stdout.write(f'Created model samples')
