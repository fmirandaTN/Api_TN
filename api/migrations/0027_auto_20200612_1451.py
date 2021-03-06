# Generated by Django 3.0.5 on 2020-06-12 14:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_project_experience_required'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='completed_works',
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 6, 19)),
        ),
        migrations.AlterField(
            model_name='project',
            name='status',
            field=models.CharField(choices=[('completed', 'completed'), ('published', 'published'), ('in_progress', 'in_progress'), ('receiving', 'receiving')], default='published', max_length=30),
        ),
    ]
