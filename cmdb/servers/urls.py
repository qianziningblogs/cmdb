#!/usr/bin/env python
# coding: utf-8 
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/4/8 14:43
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .engineroom import (
    RoomList,
    EngineCreate,
    EngineUpdateView,
)
from .cabinet import (
    CabinetList,
    CabinetCreate,
    CabinetUpdateView,
    CabinetDetailView
)
from .machine import (
    MachineList,
    MachineCreate,
    MachineDetailView,
    MachineUpdateView,
    check_floor,
    MachineTypeView,
    MachineStatusView,
    TimeLinelView
)
urlpatterns = [
    url(r'^machine/list/$', MachineList.as_view(), name='machine_list'),
    url(r'^machine/create/$', MachineCreate.as_view(), name="machine_create"),
    url(r'^machine/detail/(?P<uuid>[a-z-\d]+)/$', MachineDetailView.as_view(), name="machine_detail"),
    url(r'^machine/update/(?P<pk>[a-z-\d]+)/$', MachineUpdateView.as_view(), name="machine_update"),
    url(r'^room/list/$', RoomList.as_view(), name='room_list'),
    url(r'^room/create/$', EngineCreate.as_view(), name='room_create'),
    url(r'^cabinet/list/$', CabinetList.as_view(), name='cabinet_list'),
    url(r'^cabinet/create/$', CabinetCreate.as_view(), name='cabinet_create'),
    url(r'^cabinet/detail/(?P<pk>[\d]+)/$', CabinetDetailView.as_view(), name='cabinet_detail'),
    url(r'^cabinet/update/(?P<pk>[\d]+)/$', CabinetUpdateView.as_view(), name="cabinet_update"),
    url(r'^timeline/list/(?P<pk>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})/$', TimeLinelView.as_view(), name="timeline_list"),
    url(r'^room/update/(?P<id>[\d]+)/$', EngineUpdateView.as_view(), name="room_update"),
    url(r'check_floor', check_floor, name='check_floor'),
    url(r'^machine/type/$', MachineTypeView.as_view(), name="machine_type"),
    url(r'^machine/status/$', MachineStatusView.as_view(), name="machine_status")
]
