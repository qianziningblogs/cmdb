#!/usr/bin/env python
# coding: utf-8 
# @Time   : network.py
# @Author : Derek
# @File   : 2018/4/10 10:10


from __future__ import absolute_import, unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin, FieldClassMixin
from .models import Network
from .forms import NetworkCreateForm,NetworkUpdateForm


class NetworkList(LoginRequiredMixin, CommonMixin, ListView):
    module=Network
    template_name = 'network/network.html'
    paginate_by = '10'
    context_object_name = 'networks'
    page_title = '网络设备列表'

    def get_queryset(self):
        name = self.request.GET.get('name')
        networks = Network.objects
        if name:
            networks = networks.filter(name__contains=name)
        return networks.all()


class NetworkCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'network/network_create.html'
    page_title = '网络设备创建'
    form_class = NetworkCreateForm
    success_url = reverse_lazy('network:network_list')


class NetworkDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = Network
    template_name = 'network/network_detail.html'
    page_title = '设备详情'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'

    def get_template_names(self):
        tab = self.request.GET.get('tab')
        if tab == 'inter':
            return ["network/network_detail_baseinfo.html"]
        else:
            return ["network/network_detail_baseinfo.html"]

    def get_context_data(self, **kwargs):
        context = super(NetworkDetailView, self).get_context_data(**kwargs)
        return context


class NetworkUpdateView(LoginRequiredMixin, JsonFormMixin, UpdateView):
    model = Network
    template_name = "network/network_update.html"
    form_no_request = True
    form_type = 'update'
    slug_field = 'uuid'
    slug_url_kwarg = 'uuid'
    form_class = NetworkUpdateForm