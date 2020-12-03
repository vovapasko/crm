from django.contrib import admin
from .models import User, NewsEmail, WaveFormation, News

admin.site.register(User)
admin.site.register(NewsEmail)
admin.site.register(WaveFormation)
admin.site.register(News)
