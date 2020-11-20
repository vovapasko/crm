# Generated by Django 3.0.8 on 2020-09-23 10:50

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Credentials',
            fields=[
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=200, verbose_name='token')),
                ('refresh_token', models.CharField(max_length=200, verbose_name='refresh_token')),
                ('token_uri', models.CharField(max_length=200, verbose_name='token_uri')),
                ('client_id', models.CharField(max_length=200, verbose_name='client_id')),
                ('client_secret', models.CharField(max_length=200, verbose_name='client_secret')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Scopes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('scope', models.CharField(max_length=200, verbose_name='scope')),
                ('credentials', models.ForeignKey(db_column='Credentials.id', on_delete=django.db.models.deletion.CASCADE, to='email_app.Credentials')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
