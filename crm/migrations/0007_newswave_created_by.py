# Generated by Django 3.0.3 on 2020-06-10 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_auto_20200608_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='newswave',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
