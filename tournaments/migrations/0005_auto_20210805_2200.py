# Generated by Django 3.2.5 on 2021-08-05 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tournaments', '0004_tournamentmodel_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentmodel',
            name='required_rank',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='tournamentmodel',
            name='slots',
            field=models.IntegerField(default=25),
        ),
        migrations.CreateModel(
            name='TeamsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1', models.CharField(max_length=10)),
                ('player2', models.CharField(max_length=10)),
                ('player3', models.CharField(max_length=10)),
                ('player4', models.CharField(max_length=10)),
                ('leader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leader', to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teams', to='tournaments.tournamentmodel')),
            ],
        ),
    ]
