# Generated by Django 3.0.5 on 2020-04-27 21:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200427_1958'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_photo',
            field=models.ImageField(blank=True, upload_to=b'../images/profiles_photos'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 27, 21, 10, 21, 641692)),
        ),
    ]