# Generated by Django 3.2.7 on 2021-11-04 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0003_alter_userinfomodel_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfomodel',
            name='profile_image',
            field=models.ImageField(blank=True, upload_to='user_profile'),
        ),
    ]
