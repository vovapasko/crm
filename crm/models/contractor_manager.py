from django.db import models

from .post_format_list import PostFormatList


class ContractorManager(models.Manager):
    def create_contractor(self, editor_name: str, contact_person: str, phone_number: str, email: str):
        contractor = self.create(
            editor_name=editor_name,
            contact_person=contact_person,
            phone_number=phone_number,
            email=email
        )
        self.__create_post_format_list(contractor)
        return contractor

    def __create_post_format_list(self, contractor):
        pfl_dict = [
            {
                "contractor": contractor,
                "post_format": "article",
                "news_amount": 0,
                "arranged_news": 0,
                "one_post_price": 0,
            },
            {
                "contractor": contractor,
                "post_format": "blog",
                "news_amount": 0,
                "arranged_news": 0,
                "one_post_price": 0,
            },
            {
                "contractor": contractor,
                "post_format": "news",
                "news_amount": 0,
                "arranged_news": 0,
                "one_post_price": 0,
            }
        ]
        PostFormatList.objects.bulk_create([PostFormatList(**element) for element in pfl_dict])
