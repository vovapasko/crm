from crm.tests.base_test_case import BaseTestCase
from crm.models import Contractor
from crm.models import NewsWavePriceList, NewsWave
from django.forms.models import model_to_dict
from django.db.utils import DataError, IntegrityError


class NewsWavePriceListTestCase(BaseTestCase):
    negative_price = -1
    zero_price = 0
    good_price = 1
    upper_bound_price = 2147483647
    too_high_price = upper_bound_price + 1

    fields_to_check = ['news_wave', 'contractor', 'price']

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_contractor = Contractor.objects.first()
        cls.test_wave = NewsWave.objects.first()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_successful_create_price_list(self):
        self.__test_successful_create(price=self.good_price)
        self.__test_successful_create(price=self.zero_price)
        self.__test_successful_create(price=self.upper_bound_price)

    def test_failed_no_contractor(self):
        self.__test_failed_create(
            exception=IntegrityError,
            price=self.good_price
        )

    def test_failed_no_news_wave(self):
        self.__test_failed_create(
            exception=IntegrityError,
            price=self.good_price,
            contractor=self.test_contractor
        )

    def test_failed_create_price_list(self):
        self.__test_failed_create(
            exception=DataError,
            price=self.too_high_price,
            contractor=self.test_contractor
        )

    def __test_failed_create(self, *, exception, price=None, contractor=None):
        pl = NewsWavePriceList(
            contractor=contractor,
            price=price
        )
        self.check_with_exception(
            exception=exception,
            function=pl.save)

    def __test_successful_create(self, price):
        pl = NewsWavePriceList(
            news_wave=self.test_wave,
            contractor=self.test_contractor,
            price=price
        )
        pl.save()
        self.check_keys_in_dict(data=model_to_dict(pl), keys_to_check=self.fields_to_check)
