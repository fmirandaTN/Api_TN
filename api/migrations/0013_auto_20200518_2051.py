# Generated by Django 3.0.5 on 2020-05-18 20:51

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20200515_0200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='api.Client'),
        ),
        migrations.AlterField(
            model_name='request',
            name='collaborator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='api.Collaborator'),
        ),
        migrations.AlterField(
            model_name='request',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='api.Project'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 18, 20, 51, 5, 47977)),
        ),
    ]
