from django.db import models
from utils.jsonfield import JSONField
# Create your models here.

class AnsibleTasks(models.Model):
    '''
    playbook: 执行自定义playbook
    '''
    
    TASK_STATUS_CHOICES = (
        ('0', "未开始"),
        ('1', '执行中'),
        ('2', '已完成'),
        ('3', '执行失败'),
    )
    
    task_name = models.CharField(verbose_name="任务名称", unique=True, max_length=64)
    task_describe = models.CharField(verbose_name="任务描述", max_length=256)
    task_machines = models.TextField(verbose_name="任务机器")
    task_status = models.CharField(verbose_name="任务状态", max_length=3, choices=TASK_STATUS_CHOICES, default="0")
    playbook_name = models.CharField(max_length=64, blank=True, null=True)
    playbook_content = models.TextField()
    create_user = models.CharField(verbose_name="创建者", max_length=64)
    create_at = models.DateTimeField(auto_now_add=True)
    finish_at = models.DateTimeField(auto_now=True)
    task_result = JSONField(verbose_name="执行结果", max_length=-1)
    
    class Meta:
        ordering = ("-create_at",)



class CrontabTasks(models.Model):
    
    STATUS = (
        ("0", "未添加"),
        ("1", "执行中"),
        ("2", "已添加"),
        ("3", "添加失败"),
        ("4", "已删除"),
    )
    
    cron_name = models.CharField(verbose_name="计划名称", unique=True, max_length=64)
    cron_describe = models.CharField(verbose_name="计划描述", max_length=256)
    cron_machines = models.TextField(verbose_name="任务机器")
    task_status = models.CharField(verbose_name="计划状态",choices=STATUS, max_length=1, default="0")
    cron_schedule = JSONField()
    cmd = models.TextField()
    run_user = models.CharField(verbose_name="计划所属用户", max_length=64, default="root")
    playbook_name = models.CharField(max_length=64, blank=True, null=True)
    playbook_content = models.TextField(default="")
    create_user = models.CharField(verbose_name="创建者", max_length=64)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    task_result = JSONField(verbose_name="执行结果", max_length=-1, default={})

    
    class Meta:
        ordering = ("-create_at",)
