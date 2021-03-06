# Generated by Django 3.0.5 on 2020-08-04 20:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0070_auto_20200729_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='end_postulations',
            field=models.DateField(default=datetime.date(2020, 8, 11)),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gross_payment', models.IntegerField()),
                ('order_number', models.IntegerField()),
                ('payment_type', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='api.Project')),
            ],
        ),
    ]