#!/usr/bin/env python
# coding: utf-8 
# @Time   : views.py
# @Author : Derek
# @File   : 2018/4/8 13:24
from __future__ import absolute_import, unicode_literals
from operator import itemgetter
from datetime import datetime, timedelta
import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin

class HomeView(LoginRequiredMixin, CommonMixin, View):
    template_name = 'home.html'
    page_title = '概述'

    def get(self, request):
        return render(request, self.template_name)