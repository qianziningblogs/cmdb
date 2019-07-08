from django.db import models

# Create your models here.

type_choies = (
    ('1', '主机'),
    ('2', '网络设备'),
    ('3', '数据库'),
    ('4', '中间件'),
    ('5', 'WEB'),
    ('6', '应用'),
    ('7', '硬件'),
    ('8', '虚拟化')
)


class HostType(models.Model):
    hostid = models.CharField('zabbix hostid', max_length=100, null=True, blank=True)
    type = models.CharField('类型', max_length=100,choices=type_choies)