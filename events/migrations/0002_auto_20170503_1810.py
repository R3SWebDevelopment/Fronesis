# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-03 23:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='max_ticket_price',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=5),
        ),
        migrations.AddField(
            model_name='event',
            name='min_ticket_price',
            field=models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=5),
        ),
        migrations.AddField(
            model_name='event',
            name='tickets_available',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='event',
            name='tickets_sold',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='event',
            name='total_tickets',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='available',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='sold',
            field=models.IntegerField(default=0, editable=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='status',
            field=models.CharField(default='Selling', editable=False, max_length=150),
        ),
        migrations.AddField(
            model_name='ticketsales',
            name='buyer_name',
            field=models.CharField(default='NO NAME', editable=False, max_length=150),
        ),
        migrations.AlterField(
            model_name='event',
            name='organizer',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='tickets_selling_begins_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='event',
            name='tickets_selling_ends_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='ticketsales',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets_bought', to=settings.AUTH_USER_MODEL),
        ),
    ]
