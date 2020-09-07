# Generated by Django 3.0.5 on 2020-08-19 14:53

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0074_auto_20200811_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 8, 26)),
        ),
        migrations.CreateModel(
            name='KbCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=1000)),
                ('title', models.CharField(max_length=200)),
                ('content', models.CharField(max_length=2000)),
                ('issueType', models.CharField(max_length=200)),
                ('priority', models.CharField(max_length=200)),
                ('estimate', models.CharField(max_length=200)),
                ('position', models.IntegerField()),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_kanban', to='api.Project')),
            ],
        ),
    ]
