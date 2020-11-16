from django.core.management import BaseCommand
from crm.models.news_email import NewsEmail
from email_app.library.gmai_api_view_utils import build_service
from email_app.library.gmail_api import get_labels, get_messages, \
    get_full_message, get_raw_message, get_attachment, trash_message, \
    untrash_message, delete_message, list_messages_with_label


class Command(BaseCommand):
    news_email = NewsEmail.objects.get(email='petro307302@gmail.com')
    credentials = news_email.gmail_credentials.credentials_for_service()
    service = build_service(credentials)
    user_id = news_email.email
    test_message_id = '175bb8c3b24d95c3'
    message_id = '175bb6dea657a2d7'
    attachment_id = 'ANGjdJ8u_DqwdACoXGqHDh3iGqlESdAGfXbzXDLXWzcOn_xCvRwt6kvI2HYr8QoGbeX11tHvzDe2O4XGYMvgkBZF8HmnSzzehirHm-Xb4kiIhFkT3Ekhl2XkJFudlXpLiojbZJ3Ad3ub9GYtwkpjmbQa4di9OJzg4BJ-wlsXwabjxB_vc9jLXpur0ofPqHI3FvdMXUiSGrfKLyfKaKKHhJcOpyN8G94mMxEVujAzVDKKg8qzkOp8TEIPhCXcuCv47O9I-DGTPeWwO_l9n8Ff-_yE8QeFwuXvYXYsQNitSoIOSybzHBS0JIBnQsGstcJM-R51BTLi8nJp02GsVlZQkR0X-AxNQwvhoFWVBaZ4-eMZByUrwQJruQXx3104e-lajzWRt1WcVuFgg6spk0WP'

    def handle(self, *args, **options):
        messages = self.list_message()
        print()

    def list_message(self):
        messages = list_messages_with_label(self.service, self.user_id, ['TRASH'])
        return messages

    def delete(self, message_id):
        message = delete_message(self.service, self.user_id, message_id)
        return message

    def untrash(self, message_id):
        message = untrash_message(self.service, self.user_id, message_id)
        return message

    def trash(self, message_id):
        message = trash_message(self.service, self.user_id, message_id)
        return message

    def attachment(self):
        attachment = get_attachment(self.service, self.user_id,
                                    self.message_id, self.attachment_id)
        return attachment

    def raw_message(self, message_id):
        message = get_raw_message(self.service, self.user_id, message_id)
        return message

    def full_message(self, message_id):
        message = get_full_message(self.service, self.user_id, message_id)
        return message

    def messages(self):
        messages = get_messages(self.service, self.user_id, 3)
        print(messages)

    def labels(self):
        labels = get_labels(self.service, self.user_id)
        print(labels)
