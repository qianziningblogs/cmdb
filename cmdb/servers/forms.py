from django import forms
from utils.mixin import ModelForm
from .models import Cabinet, Host, EngineRoom, Change
from storage.models import Storage
from network.models import Network
from IPpool.models import IPDetail, IPpool


class MachineCreateForm(ModelForm):
    ip = forms.ChoiceField(choices=[], label='主机ip')

    def __init__(self, *args, **kwargs):
        super(MachineCreateForm, self).__init__(*args, **kwargs)
        self.fields['ip'].choices = [(i.ip, i.ip) for i in IPDetail.objects.filter(status=True)]

    class Meta:
        model = Host
        exclude = ['os', 'os_version', 'vender', 'productname', 'sn', 'kernel', 'asset']

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
        machine = super(MachineCreateForm, self).save(commit=False)
        if commit:
            machine.save()
            ipstatus = IPDetail.objects.get(ip=self.cleaned_data['ip'])
            ipstatus.status = False
            ipstatus.save()
            Change.objects.create(ip=self.cleaned_data['ip'], note='新增', event=4)
        return machine


class CabinetCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(CabinetCreateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Cabinet
        exclude = ['create_time']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def save(self,commit=True):
        cabinet = super(CabinetCreateForm, self).save(commit=False)
        if commit:
            cabinet.save()
        return cabinet


class EngineCreateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(EngineCreateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = EngineRoom
        exclude = ['create_time']

    def clean_name(self):
        return self.cleaned_data['name'].strip()

    def save(self, commit=True):
        engine = super(EngineCreateForm,self).save(commit=False)
        if commit:
            engine.save()
        return engine

class MachineUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(MachineUpdateForm,self).__init__(*args, **kwargs)

    class Meta:
        model = Host
        fields = ['hostname', 'os', 'cabinet', 'floor', 'mange_ip', 'status', 'end_time', 'user_passwd', 'responsible',
                  'app_note', 'note','node']

    def clean_ip(self):
        ip = self.cleaned_data['ip']
        ip_exits=Host.objects.filter(ip=ip).exists()
        if ip_exits:
            raise forms.ValidationError(u"该ip已经存在")
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

