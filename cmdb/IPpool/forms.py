#!/usr/bin/env python
# coding: utf-8 
# @Time   : forms.py
# @Author : Derek
# @File   : 2018/4/12 10:20
from django import forms
from utils.mixin import ModelForm
from .models import IPpool,IPDetail


class PoolCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PoolCreateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = IPpool
        exclude = ['create_time']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_subnet(self):
        subnet=self.cleaned_data['subnet']
        subnet_exits=IPpool.objects.filter(subnet=subnet).exists()
        if subnet_exits:
            raise forms.ValidationError(u"该网段已经存在")
        return subnet

    def save(self,commit=True):
        pool = super(PoolCreateForm, self).save(commit=False)
        subnet = self.cleaned_data['subnet']
        subnet_title=".".join(subnet.split('.')[0:3])
        netmask = self.cleaned_data['netmask']
        if commit:
            pool.save()
        p = IPpool.objects.filter(subnet=subnet)[0]
        print(p)
        if netmask == '24':
            for i in range(1, 255):
                IPDetail(ip="{}.{}".format(subnet_title,str(i)),ippool=p).save()
        else:
            IPpool.objects.get(subnet=subnet).delete()
        return pool

class DetailCreateForm(ModelForm):
    start=forms.CharField(label='起始ip', max_length=100)
    end=forms.CharField(label='结束ip', max_length=100)

    def __init__(self, *args, **kwargs):
        super(DetailCreateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = IPDetail
        fields = ['ippool','start', 'end', 'note']

    def clean(self):
        start = self.cleaned_data['start'].split('.')
        end = self.cleaned_data['end'].split('.')
        ippool=self.cleaned_data['ippool'].subnet.split('.')
        if int(start[-1]) < 0:
            raise forms.ValidationError('起始ip不能小于0')
        if int(end[-1]) > 255:
            raise forms.ValidationError('结束ip不能大于255')
        if int(start[-1]) > int(end[-1]):
            raise forms.ValidationError('结束ip不能小于起始ip')
        if start[0:3] != ippool[0:3] or end[0:3] != ippool[0:3]:
            raise forms.ValidationError('网段不一致')
        for i in range(int(start[-1]), int(end[-1])+1):
            ip = "{}.{}".format('.'.join(start[0:3]), str(i))
            print(ip)
            de = IPDetail.objects.filter(ip=ip,status=False).exists()
            if de:
                raise forms.ValidationError('{}已经被占用了！'.format(ip))
        return self.cleaned_data

    def save(self):
        de_save = super(DetailCreateForm, self).save(commit=False)
        start = self.cleaned_data['start'].split('.')
        end = self.cleaned_data['end'].split('.')
        for i in range(int(start[-1]), int(end[-1]) + 1):
            ip = "{}.{}".format('.'.join(start[0:3]), str(i))
            de = IPDetail.objects.get(ip=ip)
            de.status = False
            de.note = self.cleaned_data['note']
            de.save()
        return de_save