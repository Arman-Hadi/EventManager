# Generated by Django 3.2.13 on 2022-05-11 20:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20220511_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 20, 14, 0, 488862, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 20, 14, 0, 488888, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='webhookmessage',
            name='recieved_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 11, 20, 14, 0, 485675, tzinfo=utc), help_text='When message has recieved.'),
        ),
    ]
