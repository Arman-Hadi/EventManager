# Generated by Django 3.2.13 on 2022-05-11 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_user_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
