#!/usr/bin/env python
# coding: utf-8 
# @Time   : get_uuid.py
# @Author : Derek
# @File   : 2018/4/12 15:09

from django import template
from servers.models import Network

register = template.Library()

@register.simple_tag
def get_uuid(ip):
    try:
        network=Network.objects.get(ipv4__exact=ip)
        return network.host_id
    except Exception as e:
        return ''