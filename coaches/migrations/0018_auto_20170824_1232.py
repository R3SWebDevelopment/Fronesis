# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-24 17:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0017_auto_20170824_1214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coach',
            options={'permissions': (('edit_my_services', 'Edit My Service'), ('edit_contact_info', 'Edit Contact Info'), ('edit_blocked_hours', 'Edit Blocked Hours'), ('edit_booking_settings', 'Edit Booking Settings'), ('edit_venues', 'Edit Venues'))},
        ),
    ]
