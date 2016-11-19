# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_halls_and_bookings'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hall',
            old_name='not_availble',
            new_name='not_available',
        ),
        migrations.RemoveField(
            model_name='scheduleconfig',
            name='end_day',
        ),
        migrations.RemoveField(
            model_name='scheduleconfig',
            name='slots',
        ),
        migrations.RemoveField(
            model_name='scheduleconfig',
            name='start_day',
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 19, 16, 43, 34, 274923, tzinfo=utc), help_text=b'The end date of the last exam and the end time of the last session in each day.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='exam_period',
            field=models.PositiveSmallIntegerField(default=2, help_text=b'Set it to 2 For if for example, your university uses a 2-hours exam period'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 19, 16, 43, 47, 798935, tzinfo=utc), help_text=b'The start date of the first exam and the start time of the first session in each day.'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='TimeSlot',
        ),
    ]
