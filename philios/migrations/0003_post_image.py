# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-13 17:49
from __future__ import unicode_literals

from django.db import migrations, models
import philios.models


class Migration(migrations.Migration):

    dependencies = [
        ('philios', '0002_uploadedimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=philios.models.generate_upload_path),
        ),
    ]