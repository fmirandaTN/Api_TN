# Generated by Django 3.0.5 on 2020-07-23 14:21

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0062_auto_20200722_2229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 7, 30)),
        ),
    ]
