# Generated by Django 3.0.8 on 2020-11-17 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0026_auto_20201110_0831'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsWaveAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('name', models.CharField(max_length=200)),
                ('base_64', models.TextField()),
                ('type', models.CharField(max_length=200)),
                ('news', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.News')),
                ('wave_formation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.WaveFormation')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
