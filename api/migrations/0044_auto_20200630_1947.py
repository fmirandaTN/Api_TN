# Generated by Django 3.0.5 on 2020-06-30 19:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0043_auto_20200630_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='picture',
            name='project',
        ),
        migrations.RemoveField(
            model_name='picture',
            name='type',
        ),
    ]
