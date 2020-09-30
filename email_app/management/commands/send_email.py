from django.core.management.base import BaseCommand
from email_app.library.gmail_helpers import send_gmail_message
from pathlib import Path


class Command(BaseCommand):
    def handle(self, *args, **options):
        file1 = Path('README.md')
        file2 = Path('requirements.txt')
        text = 'Hello from Django with attachments'
        subject = 'Test Django'
        mail_from = 'mailfrom@gmail.com'
        mail_to = 'mailto@gmail.com'
        send_gmail_message(
            email_from=mail_from,
            email_to=mail_to,
            subject=subject,
            message_text=text,
            attachments=[file1, file2]
        )
