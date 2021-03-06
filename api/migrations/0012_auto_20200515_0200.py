# Generated by Django 3.0.5 on 2020-05-15 02:00

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20200507_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 15, 2, 0, 38, 716176)),
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_type', models.CharField(default='', max_length=20)),
                ('status', models.CharField(default='created', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='api.Client')),
                ('collaborator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='api.Collaborator')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='api.Project')),
            ],
        ),
    ]
