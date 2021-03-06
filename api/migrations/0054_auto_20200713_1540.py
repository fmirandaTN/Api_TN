# Generated by Django 3.0.5 on 2020-07-13 15:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0053_service_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='picture',
            old_name='upload',
            new_name='url',
        ),
        migrations.AddField(
            model_name='picture',
            name='file',
            field=models.FileField(default='assa', upload_to=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 7, 20)),
        ),
    ]
