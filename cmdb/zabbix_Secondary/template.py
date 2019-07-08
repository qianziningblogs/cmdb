#!/usr/bin/env python
# coding: utf-8 
# @Time   : template.py
# @Author : Derek
# @File   : 2018/5/25 09:45

from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin,FieldClassMixin
from auto.zabbix import get_template

class TemplateList(LoginRequiredMixin, CommonMixin, ListView):
    # module=Storage
    template_name = 'zabbix_Seceodary/template_list.html'
    paginate_by = '20'
    context_object_name = 'templates'
    page_title = '模版列表'

    def get_queryset(self):
        return get_template
