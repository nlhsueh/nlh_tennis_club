# Generated by Django 4.2.2 on 2024-05-23 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('M', '男性'), ('F', '女性')], max_length=10, null=True),
        ),
    ]