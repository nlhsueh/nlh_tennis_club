from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_age'),
        ('courts', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = []
