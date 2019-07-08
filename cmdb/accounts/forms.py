#!/usr/bin/env python
# coding: utf-8 
# @Time   : forms.py
# @Author : Derek
# @File   : 2018/4/8 10:16
from __future__ import absolute_import, unicode_literals
from django import forms
from django.contrib import auth
from utils.mixin import ModelForm
from servers.models import Team


class LoginForm(forms.Form):
    username = forms.CharField(max_length=36, required=True, error_messages={'required': '用户名不能为空','max_length': '用户名长度不能大于36'})
    password = forms.CharField(max_length=50, strip=False, widget=forms.PasswordInput, required=True, error_messages={'required': '密码不能为空','max_length': '密码长度不能大于36'})

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(u'账号密码不匹配')
            elif not self.user_cache.is_active:
                raise forms.ValidationError(u'此账号已被禁用')
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class TeamCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TeamCreateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Team
        fields = '__all__'

    def clean_name(self):
        name_exist = Team.objects.filter(name=self.cleaned_data['name']).exists()
        if name_exist:
            raise forms.ValidationError(u"该项目组已经存在")
        return self.cleaned_data['name'].strip()

    def save(self, commit=True):
        team = super(TeamCreateForm, self).save(commit=False)
        if commit:
            team.save()
        return team