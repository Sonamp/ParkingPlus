# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ParkingApp', '0003_auto_20150307_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carentryexit',
            name='feePaid',
            field=models.FloatField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='carentryexit',
            name='timeExit',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
