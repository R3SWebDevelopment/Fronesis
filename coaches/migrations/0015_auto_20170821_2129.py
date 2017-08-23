# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-22 02:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0014_auto_20170821_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bundle',
            name='half_hour_session',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='hour_session',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='bundle',
            name='open_session',
            field=models.IntegerField(default=0, null=True),
        ),
    ]