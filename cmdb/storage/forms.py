#!/usr/bin/env python
# coding: utf-8 
# @Time   : forms.py
# @Author : Derek
# @File   : 2018/4/13 11:07
from django import forms
from utils.mixin import ModelForm
from .models import Storage
from servers.models import Host, Change
from network.models import Network
from IPpool.models import IPDetail, IPpool


class StorageCreateForm(ModelForm):
    mange_ip = forms.ChoiceField(choices=[], label='管理ip')

    def __init__(self, *args, **kwargs):
        super(StorageCreateForm, self).__init__(*args, **kwargs)
        self.fields['mange_ip'].choices = [(i.ip, i.ip) for i in IPDetail.objects.filter(status=True)]

    class Meta:
        model = Storage
        exclude = ['create_time', 'asset']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_mange_ip(self):
        ip = self.cleaned_data['mange_ip']
        ip_exits = Host.objects.filter(ip=ip).exists()
        if ip_exits:
            raise forms.ValidationError(u"该ip已经存在")
        ip_start = self.cleaned_data['ip'].split('.')
        ip_used = IPpool.objects.filter(subnet="{}.0".format('.'.join(ip_start[0:3]))).exists()
        if not ip_used:
            raise forms.ValidationError(u"该ip资源池不存在，请先添加ip资源池")
        return ip

    def clean_floor(self):
        floor = self.cleaned_data['floor']
        cabinet = self.cleaned_data['cabinet']
        floor_exits = Host.objects.filter(floor=floor,  cabinet=cabinet).exists()
        storage_exits = Storage.objects.filter(floor=floor, cabinet=cabinet).exists()
        network_exits = Network.objects.filter(floor=floor, cabinet=cabinet).exists()
        if floor_exits or storage_exits or network_exits:
            raise forms.ValidationError(u"该位置已经有设备存在")
        return floor

    def save(self,commit=True):
        storage = super(StorageCreateForm, self).save(commit=False)
        if commit:
            storage.save()
            ipstatus = IPDetail.objects.get(ip=self.cleaned_data['ip'])
            ipstatus.status = False
            ipstatus.save()
            Change.objects.create(ip=self.cleaned_data['ip'], note='新增', event=4)
        return storage


class StorageUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(StorageUpdateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Storage
        fields = ['cabinet', 'floor', 'disk_type', 'disk_num', 'inter_type', 'inter_num', 'maintenance']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_floor(self):
        floor = self.cleaned_data['floor']
        cabinet = self.cleaned_data['cabinet']
        floor_exits = Host.objects.filter(floor=floor,  cabinet=cabinet).exists()
        storage_exits = Storage.objects.filter(floor=floor, cabinet=cabinet).exists()
        network_exits = Network.objects.filter(floor=floor, cabinet=cabinet).exists()
        if floor_exits or storage_exits or network_exits:
            raise forms.ValidationError(u"该位置已经有设备存在")
        return floor

    def save(self,commit=True):
        storage = super(StorageUpdateForm, self).save(commit=False)
        if commit:
            storage.save()
        return storage
