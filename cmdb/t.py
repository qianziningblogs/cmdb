#!/usr/bin/env python
# coding: utf-8 
# @Time   : t.py
# @Author : Derek
# @File   : 2018/4/3 15:12
import requests
# from servers.models import Host
# for i in Host.objects.all():
#     print(i)
# base_url="http://{}/instances/api/host/instances/?token=cmdb_api_token&hostname={}"
# def sync_machine():
#     host_all=Host.objects.filter(asset_type="1")
#     for host in host_all:
#         base_url.format('127.0.0.1:8880', host.hostname)
#         res = requests.get(base_url)
#         r = res.text
#         for i in r['data']:
#             h = Host.objects.filter(ip=i)
#             print(h)

# sync_machine()
import json
base_url = "http://{}/instances/api/host/instances/?token=cmdb_api_token&hostname={}"
url = base_url.format('127.0.0.1:8880', 'ostack56.yzct.sinochem.cloud')
req = requests.get(url).text
print(json.loads(req))
for host in json.loads(req)['data']:
    print(host)