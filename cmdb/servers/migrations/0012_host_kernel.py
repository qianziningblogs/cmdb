# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-10 06:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('servers', '0011_auto_20180409_1206'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='kernel',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='内核'),
        ),
    ]
