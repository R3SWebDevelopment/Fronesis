# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-25 23:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_auto_20170824_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicepayment',
            name='auth_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='servicepayment',
            name='credit_card',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
