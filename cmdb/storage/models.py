from django.db import models
from servers.models import Cabinet
# Create your models here.

disk_type_choies = (
    ("1", "SAS"),
    ("2", "机械")
)
inter_type_choies = (
    ("1", "SAS"),
    ("2", "机械")
)
ASSET_STATUS = (
    (str(1), u"使用中"),
    (str(2), u"未使用"),
    (str(3), u"故障"),
    (str(4), u"其它"),
)

class Storage(models.Model):
    name = models.CharField('主机名', max_length=10)
    mange_ip = models.GenericIPAddressField('管理IP', unique=True)
    cabinet = models.ForeignKey(Cabinet, null=True, blank=True, verbose_name='所在机柜')
    floor = models.CharField('所在位置', max_length=100, null=True, blank=True, default="多位置以-连接")
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True)
    head = models.CharField('存储机头', max_length=10, blank=True, null=True)
    expansion = models.CharField('存储扩展柜', max_length=10, blank=True, null=True)
    disk_type = models.CharField('硬盘类型', choices=disk_type_choies, max_length=10)
    disk_num = models.CharField('硬盘数量', max_length=10, blank=True, null=True)
    inter_type = models.CharField('接口类型', choices=inter_type_choies, max_length=10)
    inter_num = models.CharField('接口数量', max_length=10, blank=True, null=True)
    maintenance = models.CharField('维保信息', max_length=10, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    u = models.IntegerField('U数', blank=True, null=True)
    note = models.CharField('备注', max_length=100, blank=True, null=True)

    class Meta:
        ordering = ['-create_time']
        unique_together = ('cabinet', 'floor')

    def __str__(self):
        return self.name
