# Generated by Django 3.0.8 on 2020-09-28 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('email_app', '0001_initial'),
        ('crm', '0020_auto_20200831_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsemail',
            name='gmail_credentials',
            field=models.ForeignKey(db_column='Credentials.id', null=True, on_delete=django.db.models.deletion.SET_NULL,
                                    to='email_app.Credentials'),
        ),
    ]
