# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-10 17:47
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170310_1100'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ppoi',
            field=versatileimagefield.fields.PPOIField(default='0.5x0.5', editable=False, max_length=20, verbose_name='Image PPOI'),
        ),
    ]
