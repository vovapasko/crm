from django.urls import path
from email_app.views import *

app_name = 'email_app'

urlpatterns = [
    path('test/', TestView.as_view(), name='test'),
]
