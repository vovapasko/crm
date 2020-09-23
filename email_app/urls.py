from django.urls import path
from email_app.views import *

app_name = 'email_app'

urlpatterns = [
    path('gmail-auth/', GmailAuthView.as_view(), name='gmail-auth'),
]
