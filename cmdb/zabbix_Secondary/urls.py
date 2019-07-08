#!/usr/bin/env python
# coding: utf-8 
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/5/21 17:32


from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import (
    HomeView,
)
from .template import (
    TemplateList
)
urlpatterns = [
    url(r'zabbix/home/$', HomeView.as_view(), name='home'),
    url(r'template/list/$', TemplateList.as_view(), name='template_list'),
]