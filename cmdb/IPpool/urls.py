#!/usr/bin/env python
# coding: utf-8 
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/4/12 09:35

from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import (
    PoolList,
    PoolCreate,
    PoolDetailView,
    DetailCreate,
)
urlpatterns = [
    url(r'^pool/list/$', PoolList.as_view(), name='pool_list'),
    url(r'^pool/create/$', PoolCreate.as_view(), name="pool_create"),
    url(r'^detail/create/$', DetailCreate.as_view(), name="detail_create"),
    url(r'^pool/detail/(?P<pk>[\d]+)/$', PoolDetailView.as_view(), name="pool_detail"),
    # url(r'^cust/create/$', MachineCreate.as_view(), name="cust_create"),

]
