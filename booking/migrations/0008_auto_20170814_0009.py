# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-14 05:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20170813_2327'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appointments',
            old_name='google_calender_url',
            new_name='google_calendar_url',
        ),
    ]
