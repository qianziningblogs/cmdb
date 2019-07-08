#!/usr/bin/env python
# coding: utf-8 
# @Time   : project.py
# @Author : Derek
# @File   : 2018/4/9 14:51

from __future__ import absolute_import, unicode_literals
from django.db.models import Q
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixin import CommonMixin, JsonFormMixin
from django.core.urlresolvers import reverse_lazy
from servers.models import Team
from .forms import TeamCreateForm

class TeamList(LoginRequiredMixin, CommonMixin, ListView):
    module=Team
    template_name = 'accounts/project_list.html'
    paginate_by = '10'
    context_object_name = 'teams'
    page_title = '项目组列表'

    def get_queryset(self):
        name = self.request.GET.get('name')
        teams = Team.objects
        if name:
            teams=teams.filter(name__icontains=name)
        return teams.all()



class TeamCreate(LoginRequiredMixin,CommonMixin,JsonFormMixin,CreateView):
    template_name = 'accounts/project_create.html'
    page_title = '项目组创建'
    form_class = TeamCreateForm
    success_url = reverse_lazy('accounts:team_list')