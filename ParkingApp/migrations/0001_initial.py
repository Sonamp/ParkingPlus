# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarEntryExit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('carNo', models.CharField(max_length=100)),
                ('floorNo', models.SmallIntegerField()),
                ('timeEntered', models.DateTimeField()),
                ('timeExit', models.DateTimeField()),
                ('feePaid', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FloorPlan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('floorNo', models.SmallIntegerField()),
                ('totalParking', models.IntegerField()),
                ('availableParking', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
