# Generated by Django 3.0.8 on 2020-11-10 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0025_auto_20201102_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newsattachment',
            name='file',
        ),
        migrations.AddField(
            model_name='newsattachment',
            name='base_64',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsattachment',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsattachment',
            name='type',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]