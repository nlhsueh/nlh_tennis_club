# Generated by Django 4.2.2 on 2024-04-28 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_remove_member_age_remove_member_joined_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='joined_date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]