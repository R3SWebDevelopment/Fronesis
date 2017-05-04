# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-04 00:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0002_auto_20170503_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='event',
            name='location',
        ),
        migrations.RemoveField(
            model_name='event',
            name='subtitle',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tickets_selling_begins_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='tickets_selling_ends_date',
        ),
        migrations.RemoveField(
            model_name='event',
            name='time',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.AddField(
            model_name='event',
            name='begins_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='city',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='event',
            name='display_ramaining_tickets',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='event',
            name='ends_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='name',
            field=models.CharField(default='Event Name', max_length=150),
        ),
        migrations.AddField(
            model_name='event',
            name='neighborhood',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.AddField(
            model_name='event',
            name='postal_code',
            field=models.CharField(blank=True, default='', max_length=5),
        ),
        migrations.AlterField(
            model_name='event',
            name='address',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]
