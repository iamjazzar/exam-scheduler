# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='courses',
        ),
        migrations.AddField(
            model_name='student',
            name='courses',
            field=models.ManyToManyField(to='scheduler.Course'),
        ),
    ]
