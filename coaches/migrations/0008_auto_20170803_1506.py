# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0007_auto_20170802_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='coaches.Coach'),
        ),
    ]
