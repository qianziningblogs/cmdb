#!/usr/bin/env python
# coding: utf-8
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/4/8 14:43
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from .network import (
    NetworkList,
    NetworkCreate,
    NetworkDetailView,
    NetworkUpdateView,
)

urlpatterns = [
    url(r'^network/list/$', NetworkList.as_view(), name='network_list'),
    url(r'^network/create/$', NetworkCreate.as_view(), name="network_create"),
    url(r'^network/detail/(?P<uuid>[a-z-\d]+)/$', NetworkDetailView.as_view(), name="network_detail"),
    url(r'^network/update/(?P<uuid>[a-z-\d]+)/$', NetworkUpdateView.as_view(), name="network_update"),

]