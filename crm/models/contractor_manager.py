from django.db import models
from crm.models.contractor_comment_list import ContractorCommentList
from crm.models.contractor_publications_list import ContractorPublicationsList
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
        self.__create_contractor_publications_comments_list(contractor)
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

    def __create_contractor_publications_comments_list(self, contractor):
        # by default create empty publications list and empty comment list
        comments = ContractorCommentList.objects.create(
            contractor=contractor
        )
        ContractorPublicationsList.objects.create(
            contractor=contractor
        )
