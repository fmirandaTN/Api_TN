# Generated by Django 3.0.5 on 2020-06-16 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20200615_1949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 6, 23)),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='created', max_length=20),
        ),
    ]
