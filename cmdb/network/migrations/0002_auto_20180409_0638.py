# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-09 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='network',
            name='end_time',
            field=models.DateField(blank=True, null=True, verbose_name='设备过保时间'),
        ),
        migrations.AddField(
            model_name='network',
            name='login_type',
            field=models.CharField(blank=True, choices=[('1', 'HTTP'), ('2', 'SSH'), ('3', 'TELNET')], max_length=10, null=True, verbose_name='登陆方式'),
        ),
        migrations.AddField(
            model_name='network',
            name='sn',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='sn'),
        ),
    ]
