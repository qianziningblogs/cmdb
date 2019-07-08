from django.db import models
from servers.models import Team, ASSET_STATUS,ASSET_TYPE
from IPpool.models import IPpool
from utils.jsonfield import JSONCharField
# Create your models here.


#Todo zabbix是否需要添加
class Auto(models.Model):
    name = models.CharField('名称', max_length=100)
    ippool = models.ForeignKey(IPpool, verbose_name='IP资源池')
    start_ip = models.CharField('起始地址', max_length=10, default='只填最后一位就可以')
    end_ip = models.CharField('结束地址', max_length=10, default='只填最后一位就可以')
    status = models.CharField("设备状态", choices=ASSET_STATUS, max_length=30, null=True, blank=True, default="1")
    asset_type = models.CharField("设备类型", choices=ASSET_TYPE, max_length=30, null=True, blank=True, default="1")
    team = models.ForeignKey(Team, verbose_name='所属项目')
    zabbix = JSONCharField('zabbix模版', max_length=100, blank=True, null=True)
    create_time = models.DateTimeField("创建时间", auto_now_add=True)

    class Meta:
        ordering = ['-create_time']

    def __str__(self):
        return '{}的起始地址{},结束地址{}'.format(self.name, self.start_ip, self.end_ip)