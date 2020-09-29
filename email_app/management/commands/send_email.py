from django.core.management.base import BaseCommand
from crm.models.news_email import NewsEmail
from email_app.library.gmail_helpers import create_message, send_message
from email_app.library.gmail_utils import build_service


class Command(BaseCommand):
    def handle(self, *args, **options):
        test_email = NewsEmail.objects.last()  # this email has to be real
        email = test_email.email
        message = create_message(
            sender=email,
            to='writeyourmail@gmail.com',
            subject='Test message from Django',
            message_text='Hello, I am crm from Django'
        )
        credentials = test_email.gmail_credentials
        service = build_service(credentials=credentials.credentials_for_service())
        res = send_message(service=service, user_id=email, message=message)
        print(res)
