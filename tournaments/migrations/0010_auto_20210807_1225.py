# Generated by Django 3.2.5 on 2021-08-07 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0009_remove_teamsmodel_player4'),
    ]

    operations = [
        migrations.AddField(
            model_name='teamsmodel',
            name='payment_ammount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamsmodel',
            name='player1',
            field=models.CharField(default='player', max_length=10),
        ),
        migrations.AlterField(
            model_name='teamsmodel',
            name='player2',
            field=models.CharField(default='player', max_length=10),
        ),
        migrations.AlterField(
            model_name='teamsmodel',
            name='player3',
            field=models.CharField(default='player', max_length=10),
        ),
    ]
