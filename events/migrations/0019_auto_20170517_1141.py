# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-17 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0018_auto_20170517_1122'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticket',
            options={'ordering': ['price', 'name']},
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='checkout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='email',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='line1',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='line2',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='line3',
            field=models.CharField(blank=True, default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='phone_number',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='shoppingcart',
            name='selected',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterOrderWithRespectTo(
            name='ticketselection',
            order_with_respect_to='ticket_type',
        ),
    ]