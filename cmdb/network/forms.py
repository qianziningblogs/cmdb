from django import forms
from utils.mixin import ModelForm
from .models import Network
from servers.models import Host,Change
from storage.models import Storage
from IPpool.models import IPDetail, IPpool


class NetworkCreateForm(ModelForm):

    ip = forms.ChoiceField(choices=[], label='管理ip')

    def __init__(self, *args, **kwargs):
        super(NetworkCreateForm, self).__init__(*args, **kwargs)
        self.fields['ip'].choices = [(i.ip, i.ip) for i in IPDetail.objects.filter(status=True)]

    class Meta:
        model = Network
        exclude = ['create_time']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def clean_ip(self):
        ip = self.cleaned_data['ip']
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
        floor_exits = Host.objects.filter(floor=floor, cabinet=cabinet).exists()
        storage_exits = Storage.objects.filter(floor=floor, cabinet=cabinet).exists()
        network_exits = Network.objects.filter(floor=floor, cabinet=cabinet).exists()
        if floor_exits or storage_exits or network_exits:
            raise forms.ValidationError(u"该位置已经有设备存在")
        return floor

    def save(self, commit=True):
        network = super(NetworkCreateForm, self).save(commit=False)
        if commit:
            network.save()
            ipstatus = IPDetail.objects.get(ip=self.cleaned_data['ip'])
            ipstatus.status = False
            ipstatus.save()
            Change.objects.create(ip=self.cleaned_data['ip'], note='新增', event=4)
        return network


class NetworkUpdateForm(ModelForm):

    class Meta:
        model = Network
        fields = ['cabinet', 'floor', 'status', 'asset_type', 'login_type', 'user_passwd', 'note']

    def clean_floor(self):
        floor = self.cleaned_data['floor']
        cabinet = self.cleaned_data['cabinet']
        floor_exits = Host.objects.filter(floor=floor, cabinet=cabinet).exists()
        storage_exits = Storage.objects.filter(floor=floor, cabinet=cabinet).exists()
        network_exits = Network.objects.filter(floor=floor, cabinet=cabinet).exists()
        if floor_exits or storage_exits or network_exits:
            raise forms.ValidationError(u"该位置已经有设备存在")
        return floor

    def save(self, commit=True):
        network = super(NetworkUpdateForm, self).save(commit=False)
        if commit:
            network.save()
        return network
