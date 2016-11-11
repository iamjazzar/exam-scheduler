# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0002_m2m_student_courses'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_day', models.DateField()),
                ('end_day', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exam_period', models.PositiveSmallIntegerField(help_text=b'Set it to 2 For if for example, your university uses a 2-hours exam period')),
                ('starting_time', models.TimeField(help_text=b'First exam starting hour')),
                ('closing_time', models.TimeField(help_text=b'Last exam finishing hour')),
            ],
        ),
        migrations.AddField(
            model_name='scheduleconfig',
            name='slots',
            field=models.ForeignKey(to='scheduler.TimeSlot', null=True),
        ),
    ]
