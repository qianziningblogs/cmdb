from django.db import models
from django.db.models import Q
# Create your models here.

class IPpool(models.Model):
    name = models.CharField('名称', max_length=100)
    subnet = models.GenericIPAddressField('网段')
    netmask = models.CharField('掩码位数', max_length=10, default=24)
    note = models.CharField('备注', max_length=100, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return self.subnet


class IPDetail(models.Model):
    ip = models.GenericIPAddressField('ip地址')
    ippool = models.ForeignKey(IPpool,verbose_name='网段')
    status = models.BooleanField(default=True)
    note = models.CharField('备注', max_length=100, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']
