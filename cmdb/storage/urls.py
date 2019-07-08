#!/usr/bin/env python
# coding: utf-8
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/4/8 14:43
from __future__ import absolute_import, unicode_literals
from django.conf.urls import url
from .views import (
    StorageList,
    StorageCreate,
    StorageDetailView,
    StorageUpdateView,
)
urlpatterns = [
    url(r'^storage/list/$', StorageList.as_view(), name='storage_list'),
    url(r'^storage/create/$', StorageCreate.as_view(), name="storage_create"),
    url(r'^storage/detail/(?P<pk>[\d]+)/$', StorageDetailView.as_view(), name="storage_detail"),
    url(r'^storage/update/(?P<pk>[\d]+)/$', StorageUpdateView.as_view(), name="storage_update"),

]