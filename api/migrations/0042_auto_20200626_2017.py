# Generated by Django 3.0.5 on 2020-06-26 20:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20200626_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='upload',
            field=models.CharField(max_length=250),
        ),
    ]