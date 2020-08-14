from crm.models import PostFormatList, Contractor
from crm.tests.base_test_case import BaseTestCase
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError, DataError


class PostFormatListTestCase(BaseTestCase):
    good_post_format = "format"
    _50_symbols_post_format = BaseTestCase.generate_random_string(length=PostFormatList.max_post_format_length)
    # more than 50 symbols
    too_long_post_format = BaseTestCase.generate_random_string(length=PostFormatList.max_post_format_length + 1)
    keys_to_check = ['contractor', 'post_format', 'news_amount', 'arranged_news', 'one_post_price']

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.test_contractor = Contractor.objects.first()

    @classmethod
    def tearDownClass(cls) -> None:
        super().tearDownClass()

    def test_less_50_symbols_postformat_create(self):
        self.__test_good_postformat_create(self.good_post_format)

    def test_50_symbols_postformat(self):
        self.__test_good_postformat_create(self._50_symbols_post_format)

    def __test_good_postformat_create(self, format: str):
        pf = PostFormatList(
            contractor=self.test_contractor,
            post_format=format
        )
        pf.save()
        self.check_keys_in_dict(data=model_to_dict(pf), keys_to_check=self.keys_to_check)

    def test_no_contractor_postformat_create(self):
        pf = PostFormatList(
            post_format=self.good_post_format
        )
        self.check_with_exception(exception=IntegrityError, function=pf.save)

    def test_no_postformat_postformat_create(self):
        pf = PostFormatList(
            contractor=self.test_contractor
        )
        self.check_with_exception(exception=IntegrityError, function=pf.save)

    def test_too_long_postformat_postformat_create(self):
        pf = PostFormatList(
            post_format=self.too_long_post_format,
            contractor=self.test_contractor
        )
        self.check_with_exception(exception=DataError, function=pf.save)

