# Generated by Django 3.0.5 on 2020-08-11 22:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0073_auto_20200810_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 8, 18)),
        ),
    ]
