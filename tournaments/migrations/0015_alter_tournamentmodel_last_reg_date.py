# Generated by Django 3.2.5 on 2021-08-09 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0014_auto_20210809_2156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournamentmodel',
            name='last_reg_date',
            field=models.DateField(),
        ),
    ]
