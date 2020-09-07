# Generated by Django 3.0.5 on 2020-04-24 21:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20200424_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skill',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill', to='api.Category'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 24, 21, 18, 31, 97708)),
        ),
    ]
