# Generated by Django 4.2.2 on 2024-05-23 14:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courts', '0004_alter_booking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='date',
            field=models.DateField(default=datetime.date(2024, 5, 23)),
        ),
    ]