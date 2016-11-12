# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0003_schedule_configs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hall',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hall_number', models.CharField(help_text=b'The unique hall number', unique=True, max_length=16)),
                ('not_availble', models.BooleanField(help_text=b"Check if this hall cannot hold exam sessions whether it's booked or not.")),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='HallBooking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.DateTimeField(help_text=b'The start date and time the hall is booked in.')),
                ('end', models.DateTimeField(help_text=b'The last date and time the hall is booked in.')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('hall', models.ForeignKey(to='scheduler.Hall')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 11, 17, 558380, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 11, 26, 850666, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 11, 31, 371184, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='maximum_daily_exams',
            field=models.PositiveSmallIntegerField(default=2, help_text=b'A fairness requirement that each student shall not have more exams than it per day.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='maximum_gap',
            field=models.PositiveSmallIntegerField(default=2, help_text=b'A student shall not have a gap of more than the specified days between two successive exams (another fairness requirement).'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 11, 57, 679078, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 12, 0, 987041, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 12, 3, 599944, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeslot',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 12, 5, 659866, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='timeslot',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 12, 13, 12, 9, 224849, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(help_text=b'The current courses this student enrolls in.', to='scheduler.Course'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='closing_time',
            field=models.TimeField(help_text=b'Last exam finishing hour.'),
        ),
        migrations.AlterField(
            model_name='timeslot',
            name='starting_time',
            field=models.TimeField(help_text=b'First exam starting hour.'),
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='halls',
            field=models.ManyToManyField(help_text=b'The halls the exams will be held in.', to='scheduler.Hall'),
        ),
    ]
