# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-24 17:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0029_auto_20170705_1036'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['begins_date', 'begins_time'], 'permissions': (('edit_event', 'Edit Event'), ('create_event', 'Create Event'))},
        ),
    ]
