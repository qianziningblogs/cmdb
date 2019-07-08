#!/usr/bin/env python
# coding: utf-8 
# @Time   : urls.py
# @Author : Derek
# @File   : 2018/4/8 10:13
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.core.urlresolvers import reverse_lazy
from .forms import LoginForm
from .project import (
    TeamList,
    TeamCreate,
)

urlpatterns = [
    url(r'^login/$', login, {'authentication_form': LoginForm, 'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'next_page': reverse_lazy('accounts:login')}, name='logout'),
    url(r'team/list/$',TeamList.as_view(),name='team_list'),
    url(r'team/create/$',TeamCreate.as_view(),name='team_create'),
]
