# Generated by Django 3.0.5 on 2020-07-27 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_auto_20200727_1343'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='File',
            new_name='ProjectFile',
        ),
    ]
