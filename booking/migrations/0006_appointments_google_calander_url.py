# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-11 00:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_auto_20170807_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointments',
            name='google_calander_url',
            field=models.URLField(null=True),
        ),
    ]