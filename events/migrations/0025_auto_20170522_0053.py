# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-22 05:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_auto_20170521_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentcreditcard',
            name='uuid',
            field=models.CharField(editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='paymentcustomer',
            name='uuid',
            field=models.CharField(editable=False, max_length=50),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='state',
            field=models.CharField(blank=True, choices=[('Aguascalientes', 'Aguascalientes'), ('Baja California Norte', 'Baja California Norte'), ('Baja California Sur', 'Baja California Sur'), ('Campeche', 'Campeche'), ('Chiapas', 'Chiapas'), ('Coahuila', 'Coahuila'), ('Colima', 'Colima'), ('Ciudad de México', 'Ciudad de México'), ('Durango', 'Durango'), ('Estado de México', 'Estado de México'), ('Guanajuato', 'Guanajuato'), ('Guerrero', 'Guerrero'), ('Hidalgo', 'Hidalgo'), ('Jalisco', 'Jalisco'), ('Michoacán', 'Michoacán'), ('Morelos', 'Morelos'), ('Nayarit', 'Nayarit'), ('Nuevo León', 'Nuevo León'), ('Oaxaca', 'Oaxaca'), ('Puebla', 'Puebla'), ('Queretaro', 'Queretaro'), ('Quintana Roo', 'Quintana Roo'), ('San Luis Potosí', 'San Luis Potosí'), ('Sinaloa', 'Sinaloa'), ('Sonora', 'Sonora'), ('Tabasco', 'Tabasco'), ('Tamaulipas', 'Tamaulipas'), ('Tlaxcala', 'Tlaxcala'), ('Veracruz', 'Veracruz'), ('Yucatán', 'Yucatán'), ('Zacatecas', 'Zacatecas')], default='', max_length=150, null=True, verbose_name='State'),
        ),
    ]