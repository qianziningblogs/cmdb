#!/usr/bin/env python
# coding: utf-8 
# @Time   : zabbix.py
# @Author : Derek
# @File   : 2018/5/3 13:19

from pyzabbix import ZabbixAPI

def base():
    zapi = ZabbixAPI("http://10.144.129.8/zabbix")
    zapi.login("wsh", "wsh")
    return zapi

def get_template():
    z = base()
    return [(t['templateid'], t['name']) for t in z.template.get(output="extend")]

def get_template_name(ids):
    z = base()
    if ids is not None:
        return ','.join([t['name'] for t in z.template.get(output="extend", templateids=list(ids))])
    else:
        return ''

print(get_template())