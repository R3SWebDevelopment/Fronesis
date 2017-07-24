# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-21 20:41
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0002_auto_20170720_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coach',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coaches', to=settings.AUTH_USER_MODEL),
        ),
    ]