# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-31 03:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0027_auto_20170530_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsales',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
