# Generated by Django 3.0.5 on 2020-04-25 04:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20200425_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 25, 4, 23, 14, 337057)),
        ),
    ]
