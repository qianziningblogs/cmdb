#!/usr/bin/env python
# coding: utf-8 
# @Time   : engineroom.py
# @Author : Derek
# @File   : 2018/4/8 19:32

from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin, FieldClassMixin
from .models import EngineRoom
from .forms import EngineCreateForm


class RoomList(LoginRequiredMixin, CommonMixin, ListView):
    module=EngineRoom
    template_name = 'servers/engineroom.html'
    paginate_by = '30'
    context_object_name = 'enginerooms'
    page_title = '机房列表'

    def get_queryset(self):
        return EngineRoom.objects.all()


class EngineCreate(LoginRequiredMixin, CommonMixin, JsonFormMixin, CreateView):
    template_name = 'servers/engineroom_create.html'
    page_title = '机房创建'
    form_class = EngineCreateForm
    success_url = reverse_lazy('server:room_list')


class EngineUpdateView(LoginRequiredMixin, JsonFormMixin, FieldClassMixin, UpdateView):
    model = EngineRoom
    template_name = "servers/room_update.html"
    fields = ['account_manager', 'phone', 'ip_range', 'note']
    form_no_request = True
    form_type = 'update'
    slug_field = 'id'
    slug_url_kwarg = 'id'