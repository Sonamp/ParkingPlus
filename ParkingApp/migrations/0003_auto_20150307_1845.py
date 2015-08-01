# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0002_auto_20150307_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carentryexit',
            name='floorNo',
            field=models.SmallIntegerField(),
            preserve_default=True,
        ),
    ]
