from crm.models import PostFormatList, Contractor
from crm.tests.base_test_case import BaseTestCase
from django.forms.models import model_to_dict
from django.db.utils import IntegrityError, DataError


class PostFormatListTestCase(BaseTestCase):
    good_post_format = "format"
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

    def test_good_postformat_create(self):
        pf = PostFormatList(
            contractor=self.test_contractor,
            post_format=self.good_post_format
        )
        pf.save()
        self.check_keys_in_dict(data=model_to_dict(pf), keys_to_check=self.keys_to_check)

    def test_no_contractor_postformat_create(self):
        pf = PostFormatList(
            post_format=self.good_post_format
        )
        self.__test_exception(IntegrityError, pf.save)

    def test_no_postformat_postformat_create(self):
        pf = PostFormatList(
            contractor=self.test_contractor
        )
        self.__test_exception(IntegrityError, pf.save)

    def test_too_long_postformat_postformat_create(self):
        pf = PostFormatList(
            post_format=self.too_long_post_format,
            contractor=self.test_contractor
        )
        self.__test_exception(DataError, pf.save)

    def __test_exception(self, exception, function):
        with self.assertRaises(exception):
            function()
