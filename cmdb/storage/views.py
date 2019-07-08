#!/usr/bin/env python
# coding: utf-8
# @Time   : views.py
# @Author : Derek
# @File   : 2018/4/10 10:10

from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin,FieldClassMixin
from .models import Storage
from .forms import StorageCreateForm,StorageUpdateForm


class StorageList(LoginRequiredMixin, CommonMixin, ListView):
    module=Storage
    template_name = 'storage/storage.html'
    paginate_by = '10'
    context_object_name = 'storages'
    page_title = '存储列表'

    def get_queryset(self):
        name = self.request.GET.get('name')
        storages = Storage.objects
        if name:
            storages = storages.filter(name__contains=name)
        return storages.all()


class StorageCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'storage/storage_create.html'
    page_title = '存储创建'
    form_class = StorageCreateForm
    success_url = reverse_lazy('storage:storage_list')


class StorageDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = Storage
    template_name = 'storage/storage_detail.html'
    page_title = '设备详情'
    slug_field = 'pk'
    slug_url_kwarg = 'pk'

    def get_template_names(self):
        tab = self.request.GET.get('tab')
        if tab == 'inter':
            return ["storage/storage_detail_baseinfo.html"]
        else:
            return ["storage/storage_detail_baseinfo.html"]

    def get_context_data(self, **kwargs):
        context = super(StorageDetailView, self).get_context_data(**kwargs)
        return context

class StorageUpdateView(LoginRequiredMixin, JsonFormMixin, UpdateView):
    model = Storage
    form_class = StorageUpdateForm
    template_name = "storage/storage_update.html"
    form_no_request = True
    form_type = 'update'