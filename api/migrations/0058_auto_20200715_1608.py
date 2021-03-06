# Generated by Django 3.0.5 on 2020-07-15 16:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0057_auto_20200714_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='class_type',
            field=models.CharField(choices=[('project', 'project'), ('request', 'request'), ('service', 'service'), ('user', 'user'), ('none', 'none')], max_length=50),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 7, 22)),
        ),
    ]
