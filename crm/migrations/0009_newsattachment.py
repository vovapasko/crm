# Generated by Django 3.0.3 on 2020-06-11 11:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_news_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('file', models.FileField(upload_to='crm\\news_attachments')),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.News')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
