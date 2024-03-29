# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-24 18:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coaches', '0004_coach_google_calender_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='length_hours',
            field=models.IntegerField(choices=[(0, '0 hour'), (1, '1 hour'), (2, '2 hours'), (3, '3 hours'), (4, '4 hours'), (5, '5 hours'), (6, '6 hours'), (7, '7 hours'), (8, '8 hours'), (9, '9 hours'), (10, '10 hours'), (11, '11 hours'), (12, '12 hours'), (13, '13 hours'), (14, '14 hours'), (15, '15 hours'), (16, '16 hours')], default=0),
        ),
        migrations.AlterField(
            model_name='session',
            name='length_minutes',
            field=models.IntegerField(choices=[(0, '0 minute'), (1, '1 minute'), (2, '2 minutes'), (3, '3 minutes'), (4, '4 minutes'), (5, '5 minutes'), (6, '6 minutes'), (7, '7 minutes'), (8, '8 minutes'), (9, '9 minutes'), (10, '10 minutes'), (11, '11 minutes'), (12, '12 minutes'), (13, '13 minutes'), (14, '14 minutes'), (15, '15 minutes'), (16, '16 minutes'), (17, '17 minutes'), (18, '18 minutes'), (19, '19 minutes'), (20, '20 minutes'), (21, '21 minutes'), (22, '22 minutes'), (23, '23 minutes'), (24, '24 minutes'), (25, '25 minutes'), (26, '26 minutes'), (27, '27 minutes'), (28, '28 minutes'), (29, '29 minutes'), (30, '30 minutes'), (31, '31 minutes'), (32, '32 minutes'), (33, '33 minutes'), (34, '34 minutes'), (35, '35 minutes'), (36, '36 minutes'), (37, '37 minutes'), (38, '38 minutes'), (39, '39 minutes'), (40, '40 minutes'), (41, '41 minutes'), (42, '42 minutes'), (43, '43 minutes'), (44, '44 minutes'), (45, '45 minutes'), (46, '46 minutes'), (47, '47 minutes'), (48, '48 minutes'), (49, '49 minutes'), (50, '50 minutes'), (51, '51 minutes'), (52, '52 minutes'), (53, '53 minutes'), (54, '54 minutes'), (55, '55 minutes'), (56, '56 minutes'), (57, '57 minutes'), (58, '58 minutes'), (59, '59 minutes')], default=0),
        ),
        migrations.AlterField(
            model_name='venue',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='venues', to='coaches.Coach'),
        ),
    ]
