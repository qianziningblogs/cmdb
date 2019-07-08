#!/usr/bin/env python
# coding: utf-8
# @Time   : tasks.py
# @Author : Derek
# @File   : 2018/4/17 10:38

from __future__ import absolute_import, unicode_literals
from servers.models import Host
import requests
from cmdb.celery import app as celery_app
import logging
import json
from servers.models import Host

base_url = "http://{}/instances/api/host/instances/?token=cmdb_api_token&hostname={}"
_log = logging.getLogger(__name__)


@celery_app.task(bind=True, queue='cmdb')
def sync_machine():
    _log.info('Start sync_image')
    host_all=Host.objects.filter(asset_type="1")
    for host in host_all:
        url = base_url.format('127.0.0.1:8880', host.hostname)
        req = json.loads(requests.get(url).text)
        for h in req['data']:
            try:
                hu = Host.objects.get(ip__exact=h)
                hu.node=host.hostname
                hu.save()
            except Exception as e:
                pass

    _log.info('End sync_image')
