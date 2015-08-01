# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carentryexit',
            name='floorNo',
            field=models.ForeignKey(to='ParkingApp.FloorPlan'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='floorplan',
            name='availableParking',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='floorplan',
            name='floorNo',
            field=models.SmallIntegerField(unique=True),
            preserve_default=True,
        ),
    ]
