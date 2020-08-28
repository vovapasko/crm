from crm.models import Contractor
from crm.tests.base_test_case import BaseTestCase
from .test_data import MOCK_CONTRACTOR, MOCK_CONTRACTOR1


# todo provide testing the availability of attributes such as
#  postformatlist, publications and comment list
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
        self.compare_data(compare_what=MOCK_CONTRACTOR,
                          compare_to=self.dict_from_model(contractor))

    # def test_attributes_on_create(self):
    #
    #     contractor = Contractor.objects.create_contractor(
    #         **MOCK_CONTRACTOR1
    #     )
    #     postformatlist = contractor.postformatlist_set.all()
    #     self.assertIn(
    #         member=postformatlist,
    #         container=contractor.postformatlist_set.all()
    #     )
