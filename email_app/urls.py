from django.urls import path
from email_app.views import *

app_name = 'email_app'

urlpatterns = [
    path('gmail-auth/', GmailAuthView.as_view(), name='gmail-auth'),
    path('gmail-creds-clear/', GmailCredentialsClearView.as_view(), name='gmail-creds-clear'),
    path('gmail-token-revoke/', GmailTokenRevokeView.as_view(), name='gmail-token-revoke'),
    path('inbox/', EmailInboxView.as_view(), name='inbox'),
    path('messages/', EmailGetMessageView.as_view(), name='get-message'),
    path('trash-message/', TrashMessageView.as_view(), name='trash-message'),
    path('untrash-message/', UntrashMessageView.as_view(), name='untrash-message'),
    path('remove-message/', EmailRemoveMessagesView.as_view(), name='remove-message')
]
