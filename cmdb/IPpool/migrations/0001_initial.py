# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-04-11 02:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IPDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='ip地址')),
                ('status', models.BooleanField()),
                ('note', models.CharField(max_length=100, verbose_name='备注')),
            ],
        ),
        migrations.CreateModel(
            name='IPpool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
                ('subnet', models.GenericIPAddressField(verbose_name='网段')),
                ('netmask', models.CharField(default=24, max_length=10, verbose_name='掩码位数')),
                ('note', models.CharField(max_length=100, verbose_name='备注')),
            ],
        ),
        migrations.AddField(
            model_name='ipdetail',
            name='ippool',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='IPpool.IPpool'),
        ),
    ]
