# Generated by Django 3.0.5 on 2020-05-29 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20200529_0239'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_client',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_collaborator',
        ),
    ]
