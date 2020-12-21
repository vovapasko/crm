# Generated by Django 3.0.8 on 2020-12-19 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0032_user_is_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsburstmethod',
            name='method',
            field=models.CharField(default='direct', help_text='format how to burst the news', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='main_app/users_pictures/avatar_2x.png', upload_to='main_app/users_pictures'),
        ),
    ]