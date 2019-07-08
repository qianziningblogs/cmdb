from django.db import models
import uuid
from IPpool.models import IPDetail
# Create your models here.

ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
    (str(5), u"删除"),
)

ASSET_TYPE = (
    (str(1), u"物理机"),
    (str(2), u"虚拟机"),
    (str(3), u"容器"),
)


class Team(models.Model):
    """
    项目组
    """
    name=models.CharField('项目组', max_length=100)
    contacts=models.CharField('联系人',max_length=100, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class EngineRoom(models.Model):
    """
    机房
    """
    name = models.CharField('机房名称', max_length=100, null=True, blank=True)
    address = models.CharField('机房位置', max_length=100, null=True, blank=True)
    city = models.CharField('所在城市', max_length=100, null=True, blank=True)
    floor = models.CharField('所在层数', max_length=100, null=True, blank=True)
    account_manager = models.CharField('客户经理', max_length=100, null=True, blank=True)
    phone = models.CharField('电话', max_length=100, null=True, blank=True)
    ip_range = models.CharField('ip范围', max_length=100, null=True, blank=True)
    note = models.CharField('备注', max_length=1000, null=True, blank=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Cabinet(models.Model):
    """
    机柜
    """
    name = models.CharField('机柜名称', max_length=200)
    address = models.CharField('机柜位置', max_length=200)
    engine = models.ForeignKey(EngineRoom,verbose_name='机房')
    u_number=models.IntegerField('U数', blank=True, default=48)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    note = models.CharField('描述', max_length=200, blank=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.name


class Host(models.Model):
    """
    主机列表
    """
    uuid = models.UUIDField('主机唯一ID', primary_key=True, default=uuid.uuid4)
    ip = models.GenericIPAddressField('主机IP', null=True, unique=True)
    hostname = models.CharField('主机名称', max_length=100, blank=True, null=True)
    os = models.CharField('系统类型', max_length=20, blank=True, null=True)
    os_version = models.CharField('系统版本', max_length=200, blank=True, null=True)
    kernel = models.CharField('内核版本', max_length=200, blank=True, null=True)
    cabinet = models.ForeignKey(Cabinet, null=True, blank=True, verbose_name='所属机柜')
    floor = models.CharField('所在位置', max_length=30, blank=True, null=True, default="多位置以-连接")
    mange_ip = models.GenericIPAddressField('管理IP', blank=True, null=True)
    up_time = models.DateField('上架时间', blank=True, null=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True, default="1")
    asset_type = models.CharField("设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True,default="1")
    team = models.ForeignKey(Team, null=True, blank=True, verbose_name='所属项目组')
    end_time = models.DateField('过保时间', max_length=30, blank=True, null=True)
    vender = models.CharField('厂商名称', max_length=50, blank=True, null=True)
    productname = models.CharField('机器型号', max_length=50, blank=True, null=True)
    user_passwd = models.CharField('用户名/密码', max_length=30, blank=True, null=True)
    sn = models.CharField('SN码', max_length=100, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    responsible = models.CharField('责任人', max_length=30, blank=True, null=True)
    app_note = models.CharField('应用描述', max_length=100, blank=True, null=True)
    node = models.CharField('所属主机', max_length=30, blank=True, null=True)
    u = models.IntegerField('U数', blank=True, null=True, default=2)
    note = models.CharField('备注', max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-create_time']
        unique_together = ('cabinet', 'floor')

    def __str__(self):
        return self.hostname


class Cpu(models.Model):
    """
    cpu 信息
    """
    modelname = models.CharField('型号', max_length=100)
    cores = models.CharField('每颗核数', max_length=10, null=True, blank=True)
    count = models.CharField('总核数', max_length=10, null=True, blank=True)
    phyical = models.CharField('座数', max_length=10, null=True, blank=True)
    host = models.ForeignKey(Host)
    
    
    def __str__(self):
        return '{} of {}'.format(self.modelname, self.host.hostname)


class Mem(models.Model):
    """
    内存信息
    """
    size = models.CharField('大小', max_length=100, null=True, blank=True)
    type = models.CharField('类型', max_length=100, null=True, blank=True)
    speed = models.CharField('速度', max_length=100, null=True, blank=True)
    sn = models.CharField('sn', max_length=100, null=True, blank=True)
    vender = models.CharField('厂商', max_length=100, null=True, blank=True)
    host = models.ForeignKey(Host)


class Bios(models.Model):
    """
    Bios信息
    """
    vender = models.CharField('厂商', max_length=100)
    version = models.CharField('版本号', max_length=100)
    host = models.ForeignKey(Host)
    
    
    def __str__(self):
        return '{}_{}'.format(self.vender, self.version)


class Network(models.Model):
    """
    网卡相关
    """
    dev = models.CharField('名称', max_length=100)
    mac = models.CharField('mac地址', max_length=100)
    ipv4 = models.GenericIPAddressField('ipv4地址', null=True, blank=True)
    ipv4_netmask = models.GenericIPAddressField('ipv4掩码', null=True, blank=True)
    ipv6 = models.GenericIPAddressField('ipv6地址', null=True, blank=True)
    ipv6_netmask = models.GenericIPAddressField('ipv6掩码', null=True, blank=True)
    host = models.ForeignKey(Host)


class Disk(models.Model):
    """
    硬盘相关
    """
    vender = models.CharField('厂商', max_length=100, null=True, blank=True)
    sn = models.CharField('sn码', max_length=100, null=True, blank=True)
    size = models.CharField('容量', max_length=100, null=True, blank=True)
    host = models.ForeignKey(Host)

class Change(models.Model):
    """
    变更记录
    """
    event_type_choices = (
        (1, u'硬件变更'),
        (2, u'新增配件'),
        (3, u'设备下线'),
        (4, u'设备上线'),
        (5, u'定期维护'),
        (6, u'业务上线\更新\变更'),
        (7, u'其它'),
    )
    asset_type_choices = (
        ('server', u'服务器'),
        ('network', u'网络设备'),
        ('storage', u'存储设备'),
        ('security', u'机房设备'),
        ('software', u'软件资产'),
        ('others', u'其它类'),
    )
    asset = models.CharField('类型', choices=asset_type_choices, default="server", max_length=20)
    ip = models.GenericIPAddressField('ip地址')
    note = models.CharField('记录情况', max_length=100)
    event = models.SmallIntegerField(u'事件类型', choices=event_type_choices, default=1)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

