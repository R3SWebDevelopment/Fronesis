# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-03 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointments',
            name='ends_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='coaches.Session'),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='starts_datetime',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='appointments',
            name='venue',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='coaches.Venue'),
        ),
    ]
