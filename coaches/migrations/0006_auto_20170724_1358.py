# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0005_auto_20170724_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='max_capacity',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='session',
            name='person_price',
            field=models.DecimalField(decimal_places=2, max_digits=8, null=True),
        ),
    ]
