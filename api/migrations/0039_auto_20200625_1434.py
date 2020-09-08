# Generated by Django 3.0.5 on 2020-06-25 14:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0038_proposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profession',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 7, 2)),
        ),
    ]