# Generated by Django 3.2.5 on 2021-08-18 13:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0017_tournamentmodel_start_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teamsmodel',
            name='leader',
        ),
        migrations.AddField(
            model_name='teamsmodel',
            name='leader',
            field=models.ManyToManyField(related_name='leader', to=settings.AUTH_USER_MODEL),
        ),
    ]
