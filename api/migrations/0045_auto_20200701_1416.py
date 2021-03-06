# Generated by Django 3.0.5 on 2020-07-01 14:16

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0044_auto_20200630_1947'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='number_stages',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='project',
        ),
        migrations.AddField(
            model_name='proposal',
            name='request',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='proposal_request', to='api.Request'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 7, 8)),
        ),
    ]
