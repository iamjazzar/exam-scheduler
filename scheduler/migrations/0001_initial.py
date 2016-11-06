# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=16, serialize=False, primary_key=True)),
                ('first_name', models.CharField(max_length=32, null=True, blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, blank=True)),
                ('courses', models.ForeignKey(to='scheduler.Course')),
            ],
        ),
    ]
