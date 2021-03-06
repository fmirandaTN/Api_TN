# Generated by Django 3.0.5 on 2020-08-06 21:28

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0071_auto_20200804_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_number',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 8, 13)),
        ),
        migrations.CreateModel(
            name='LogTransbank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=500)),
                ('authorization_code', models.CharField(max_length=500)),
                ('card_number', models.CharField(max_length=500)),
                ('gross_payment', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='api.Order')),
            ],
        ),
    ]
