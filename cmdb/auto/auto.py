#!/usr/bin/env python
# coding: utf-8 
# @Time   : auto..py
# @Author : Derek
# @File   : 2018/4/23 16:02

from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin, FieldClassMixin
from django.core.urlresolvers import reverse_lazy
from .models import Auto
from .forms import AutoCreateForm,AutoUpdateForm
from .zabbix import get_template_name


class AutoList(LoginRequiredMixin, CommonMixin, ListView):
    module = Auto
    template_name = 'auto/auto_list.html'
    paginate_by = '30'
    context_object_name = 'autos'
    page_title = '自动发现'

    def get_queryset(self):
        name = self.request.GET.get('name')
        autos = Auto.objects
        if name:
            autos = autos.filter(name__contains=name)
        return autos.all()


class AutoCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'auto/auto_create.html'
    page_title = '自动发现'
    form_class = AutoCreateForm
    success_url = reverse_lazy('auto:auto_list')


class AutoDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = Auto
    template_name = 'auto/auto_detail.html'
    page_title = '自动发现详情'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super(AutoDetailView, self).get_context_data(**kwargs)
        subnet = Auto.objects.filter(id=self.object.pk)[0]
        base = '.'.join(subnet.ippool.subnet.split('.')[0:3])
        context['start'] = '{}.{}'.format(base, subnet.start_ip)
        context['end'] = '{}.{}'.format(base, subnet.end_ip)
        context['zabbix'] = get_template_name(subnet.zabbix)
        return context


class AutoUpdateView(LoginRequiredMixin, JsonFormMixin, UpdateView):
    model = Auto
    template_name = "auto/auto_update.html"
    form_no_request = True
    form_type = 'update'
    form_class = AutoUpdateForm
