# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 17:00
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170310_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=''),
        ),
    ]
