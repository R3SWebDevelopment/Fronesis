# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-15 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0008_event_subtitle'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(editable=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['begins_date', 'begins_time']},
        ),
        migrations.AlterModelManagers(
            name='event',
            managers=[
                ('past', django.db.models.manager.Manager()),
            ],
        ),
    ]
