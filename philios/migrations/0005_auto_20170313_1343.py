# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 19:43
from __future__ import unicode_literals

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('philios', '0004_auto_20170313_1151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to=''),
        ),
    ]
