# Generated by Django 2.2 on 2020-01-27 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstApp', '0004_auto_20200127_1223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='endDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='startDate',
            field=models.DateField(),
        ),
    ]
