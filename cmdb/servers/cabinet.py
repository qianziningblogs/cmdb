#!/usr/bin/env python
# coding: utf-8 
# @Time   : cabinet.py
# @Author : Derek
# @File   : 2018/4/8 19:47

from __future__ import absolute_import, unicode_literals
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin, FieldClassMixin
from django.core.urlresolvers import reverse_lazy
from .models import Cabinet
from .forms import CabinetCreateForm
from servers.models import Host
from storage.models import Storage
from network.models import Network


class CabinetList(LoginRequiredMixin, CommonMixin, ListView):
    module=Cabinet
    template_name = 'servers/cabinet.html'
    paginate_by = '30'
    context_object_name = 'cabinets'
    page_title = '机柜列表'

    def get_queryset(self):
        name = self.request.GET.get('name')
        cabinets = Cabinet.objects
        if name:
            cabinets = cabinets.filter(name__contains=name)
        return cabinets.all()


class CabinetCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'servers/cabinet_create.html'
    page_title = '机柜创建'
    form_class = CabinetCreateForm
    success_url = reverse_lazy('server:cabinet_list')


class CabinetUpdateView(LoginRequiredMixin, JsonFormMixin, FieldClassMixin, UpdateView):
    model = Cabinet
    template_name = "servers/cabinet_update.html"
    fields = ['u_number', 'note']
    form_no_request = True
    form_type = 'update'


class CabinetDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = Cabinet
    template_name = 'servers/cabinet_detail.html'
    page_title = '机柜详情'

    def get_context_data(self, **kwargs):
        context = super(CabinetDetailView, self).get_context_data(**kwargs)
        all=[]
        servers = Host.objects.filter(cabinet_id=self.object.pk, asset_type="1")
        host_dict={}
        storage_dict={}
        network_dict={}
        for host in servers:
            if host.floor:
                if '-' in host.floor:
                    host_dict['flag'] = int(host.floor.split("-")[1])+1
                    host_dict['num'] = host.u if host.u else 2
                else:
                    host_dict['flag'] = int(host.floor)+1
                    host_dict['num'] = host.u if host.u else 2
                host_dict['ip'] = host.ip
        all.append(host_dict)
        storages = Storage.objects.filter(cabinet_id=self.object.pk)
        for storage in storages:
            if storage.floor:
                if '-' in storage.floor:
                    storage_dict['flag'] = int(storage.floor.split("-")[1])+1
                    storage_dict['num'] = storage.u if storage.u else 2
                else:
                    storage_dict['flag'] = int(storage.floor)+1
                    storage_dict['num'] = storage.u if storage.u else 2
                storage_dict['ip'] = storage.mange_ip
        all.append(storage_dict)
        networks = Network.objects.filter(cabinet_id=self.object.pk)
        for network in networks:
            if network.floor:
                if '-' in network.floor:
                    network_dict['flag'] = int(network.floor.split("-")[1])+1
                    network_dict['num'] = network.u if network.u else 2
                else:
                    network_dict['flag'] = int(network.floor)+1
                    network_dict['num'] = network.u if network.u else 2
                network_dict['ip'] = network.ip
        all.append(network_dict)
        context['count'] = Cabinet.objects.get(id=self.object.pk).u_number
        context['details'] = all
        return context
