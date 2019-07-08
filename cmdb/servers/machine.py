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
from .forms import MachineCreateForm, MachineUpdateForm
from .models import Host, Cpu, Mem, Disk, Network as server_network, Bios, Cabinet, Change
from report.forms import DocumentForm
from storage.models import Storage
from django.http import HttpResponse
from django.views.generic import View
from network.models import Network as NetDevice
import json


class MachineList(LoginRequiredMixin, CommonMixin, ListView):
    module = Host
    template_name = 'servers/machine_list.html'
    paginate_by = '30'
    context_object_name = 'hosts'
    page_title = '机器列表'

    def get_queryset(self):
        hostname = self.request.GET.get('hostname')
        ip = self.request.GET.get('ip')
        team = self.request.GET.get('team')
        cabinet = self.request.GET.get('cabinet')
        responsible=self.request.GET.get('responsible')
        hosts = Host.objects
        if hostname:
            hosts = hosts.filter(hostname__contains=hostname)
        if ip:
            hosts = hosts.filter(network__ipv4__exact=ip)
        if team:
            hosts = hosts.filter(team__name__icontains=team)
        if cabinet:
            hosts = hosts.filter(cabinet__name__icontains=cabinet)
        if responsible:
            hosts = hosts.filter(responsible__icontains=responsible)
        return hosts.all()

    def get_context_data(self, **kwargs):
        form = DocumentForm()
        context = super(MachineList, self).get_context_data(**kwargs)
        context['form'] = form
        return context


class MachineCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'servers/machine_create.html'
    page_title = '主机创建'
    form_class = MachineCreateForm
    success_url = reverse_lazy('server:cabinet_list')


class MachineDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = Host
    template_name = 'servers/machine_detail.html'
    page_title = '机器详情'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_template_names(self):
        tab = self.request.GET.get('tab')
        if tab == 'cpu':
            return ["servers/machine_detail_cpu.html"]
        elif tab == 'mem':
            return ["servers/machine_detail_mem.html"]
        elif tab == 'disk':
            return ["servers/machine_detail_disk.html"]
        elif tab == 'network':
            return ["servers/machine_detail_network.html"]
        elif tab == 'kvm':
            return ["servers/machine_detail_kvm.html"]
        else:
            return ["servers/machine_detail_baseinfo.html"]

    def get_context_data(self, **kwargs):
        context = super(MachineDetailView, self).get_context_data(**kwargs)
        tab = self.request.GET.get('tab')

        if tab == 'cpu':
            context['cpus'] = Cpu.objects.filter(host__uuid=self.object.uuid)
        elif tab == 'mem':
            context['mems'] = Mem.objects.filter(host__uuid=self.object.uuid)
        elif tab == 'disk':
            context['disk'] = Disk.objects.filter(host__uuid=self.object.uuid)
        elif tab == 'network':
            context['networks'] = server_network.objects.filter(host__uuid=self.object.uuid)
        elif tab == 'kvm':
            context['kvms'] = Host.objects.filter(node=self.object.hostname)
        else:
            context['bios'] = Bios.objects.filter(host__uuid=self.object.uuid)
        return context


class MachineUpdateView(LoginRequiredMixin, JsonFormMixin, FieldClassMixin, UpdateView):
    model = Host
    template_name = "servers/machine_update.html"
    fields = ['hostname', 'os', 'cabinet', 'floor', 'mange_ip', 'status', 'end_time', 'user_passwd', 'responsible', 'app_note', 'note'
              ,'node']
    form_no_request = True
    form_type = 'update'
    form_class = MachineUpdateForm


def check_floor(request):
    floor = request.GET.get('floor', '')
    cabinet = request.GET.get('cabinet', '')
    cabinet = Cabinet.objects.filter(name=cabinet)
    floor_exits = Host.objects.filter(floor=floor, cabinet=cabinet).exists()
    storage_exits = Storage.objects.filter(floor=floor, cabinet=cabinet).exists()
    network_exits = NetDevice.objects.filter(floor=floor, cabinet=cabinet).exists()
    if floor_exits or storage_exits or network_exits:
        return HttpResponse(json.dumps({'res': True}))
    else:
        return HttpResponse(json.dumps({'res': False}))


class MachineTypeView(View):
    
    def get(self, request):
        physical_machines = Host.objects.filter(asset_type="1").count()
        virtual_machines = Host.objects.filter(asset_type="2").count()
        container_machines = Host.objects.filter(asset_type="3").count()
        network_device = NetDevice.objects.all().count()
        
        return HttpResponse(json.dumps({"physical_machines": physical_machines,
                                        "virtual_machines": virtual_machines,
                                        "container_machines": container_machines,
                                        "network_device": network_device
                                        }), content_type="application/json")


class TimeLinelView(LoginRequiredMixin, CommonMixin, ListView):
    model = Change
    template_name = 'servers/timeline.html'
    page_title = '变更记录'
    context_object_name = 'lines'

    def get_queryset(self):
        ip = self.request.path_info.split("/")[-2]
        print(ip)
        return Change.objects.filter(ip=ip)


class MachineStatusView(View):
    def get(self, request):
        using = Host.objects.filter(status="1").count()
        nousing = Host.objects.filter(status="2").count()
        breakdown = Host.objects.filter(status="3").count()
        other = Host.objects.filter(status="4").count()
        
        return HttpResponse(json.dumps({"using": using,
                                        "nousing": nousing,
                                        "breakdown": breakdown,
                                        "other": other
                                        }), content_type="application/json")
    
