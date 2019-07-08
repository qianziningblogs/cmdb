from django.db import models
import uuid
from servers.models import Cabinet
# Create your models here.
ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
)

ASSET_TYPE = (
    (str(1), u"交换机"),
    (str(2), u"路由器"),
    (str(3), u"安全设备"),
)
Login_type = (
    (str(1), 'HTTP'),
    (str(2), 'SSH'),
    (str(3), 'TELNET')
)


class Network(models.Model):
    uuid = models.UUIDField('机器唯一ID', primary_key=True, default=uuid.uuid4)
    hostname = models.CharField('设备名称', max_length=100, null=True)
    ip = models.GenericIPAddressField('管理IP', null=True, unique=True)
    cabinet = models.ForeignKey(Cabinet, null=True, blank=True,verbose_name='所在机柜')
    floor = models.CharField('所在位置', max_length=100, null=True, blank=True, default="多位置以-连接")
    up_time = models.DateField('上架时间', blank=True, null=True)
    end_time = models.DateField('过保时间', blank=True, null=True)
    vender = models.CharField('厂商名称', max_length=30, blank=True, null=True)
    productname = models.CharField('设备型号', max_length=30, blank=True, null=True)
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    asset_type = models.CharField("设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True)
    login_type = models.CharField('登陆方式', choices=Login_type, max_length=10, null=True, blank=True)
    user_passwd = models.CharField('用户名/密码', max_length=30, blank=True, null=True)
    sn = models.CharField('sn', max_length=10, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    note = models.CharField('备注信息', max_length=100, null=True, blank=True)
    u = models.IntegerField('U数', blank=True, null=True)

    def __str__(self):
        return self.hostname


    class Meta:
        ordering = ['-create_time']
        unique_together = ('cabinet', 'floor')
