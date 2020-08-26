from crm.models import Contractor
from crm.tests.base_test_case import BaseTestCase
from .test_data import MOCK_CONTRACTOR


class ContractorTestCase(BaseTestCase):
    keys_to_check = list(MOCK_CONTRACTOR.keys())

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_successful_create_contractor(self):
        contractor = Contractor.objects.create_contractor(
            **MOCK_CONTRACTOR
        )
        self.check_keys_in_dict(
            data=self.dict_from_model(contractor),
            keys_to_check=self.keys_to_check
        )
