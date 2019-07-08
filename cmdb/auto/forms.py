#!/usr/bin/env python
# coding: utf-8 
# @Time   : forms.py
# @Author : Derek
# @File   : 2018/4/23 15:53

from django import forms
from utils.mixin import ModelForm
from IPpool.models import IPDetail, IPpool
from .models import Auto
from .zabbix import get_template,get_template_name


class AutoCreateForm(ModelForm):
    zabbix = forms.MultipleChoiceField(choices=[], label='zabbix模块')

    def __init__(self, *args, **kwargs):
        super(AutoCreateForm, self).__init__(*args, **kwargs)

        self.fields['zabbix'].choices = get_template

    class Meta:
        model = Auto
        exclude = ['create_time']

    def clean(self):
        start = self.cleaned_data['start_ip']
        end = self.cleaned_data['end_ip']
        if int(start) < 0:
            raise forms.ValidationError('起始ip不能小于0')
        if int(end) > 255:
            raise forms.ValidationError('结束ip不能大于255')
        if int(start) > int(end):
            raise forms.ValidationError('结束ip不能小于起始ip')
        return self.cleaned_data


class AutoUpdateForm(ModelForm):

    zabbix = forms.MultipleChoiceField(label='zabbix模块')

    def __init__(self, *args, **kwargs):
        super(AutoUpdateForm, self).__init__(*args, **kwargs)
        self.fields['zabbix'].initial = ['10771', '10767']
        self.fields['zabbix'].choices = get_template()


    class Meta:
        model = Auto
        exclude = ['create_time']

    def clean(self):
        start = self.cleaned_data['start_ip']
        end = self.cleaned_data['end_ip']
        if int(start) < 0:
            raise forms.ValidationError('起始ip不能小于0')
        if int(end) > 255:
            raise forms.ValidationError('结束ip不能大于255')
        if int(start) > int(end):
            raise forms.ValidationError('结束ip不能小于起始ip')
        return self.cleaned_data