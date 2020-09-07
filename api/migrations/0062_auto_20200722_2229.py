# Generated by Django 3.0.5 on 2020-07-22 22:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0061_auto_20200722_1526'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='proposal',
            name='payment_completed',
        ),
        migrations.RemoveField(
            model_name='proposal',
            name='stage_completed',
        ),
        migrations.CreateModel(
            name='ProjectStage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1000)),
                ('price', models.IntegerField()),
                ('completed', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stage', to='api.Project')),
            ],
        ),
    ]
