import json
import os
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import CrontabTasks
from servers.models import Host
from utils.mixin import CommonMixin
from .tasks import execute_playbook
import logging
logger_error = logging.getLogger('dev_error.prod_error')
# Create your views here.

import os

PLAYBOOK_BASE_PATH = os.path.join("/tmp/",'playbook')

class CronTasksList(LoginRequiredMixin, CommonMixin, ListView):
    module = CrontabTasks
    template_name = 'scheduler/crontabtask_list.html'
    paginate_by = '15'
    context_object_name = 'tasks'
    page_title = '计划列表'
    
    def get_queryset(self):
        tasks = CrontabTasks.objects.all()

        cron_name = self.request.GET.get("cron_name", "")
        if cron_name:
            tasks = tasks.filter(cron_name__icontains=cron_name)
            
        task_status = self.request.GET.get("task_status", "")
        if task_status:
            tasks = tasks.filter(task_status=task_status)
        return tasks


class CronCreateView(LoginRequiredMixin, CommonMixin, View):
    def get(self, request):
        page_title = '任务创建'
        machines = Host.objects.all()
        return render(request, "scheduler/crontabtask_create.html", {"html": "<em><b>脚本预览......</b></em>",
                                                                     "page_title": page_title,
                                                                     "machines": machines})
        
    def post(self, request):
        minute = request.POST.get("minute", "*")
        hour = request.POST.get("hour", "*")
        day = request.POST.get("day", "*")
        month = request.POST.get("month", "*")
        weekday = request.POST.get("weekday", "*")
        user = request.POST.get("user", "root")
        cronname = request.POST.get("cronname", "")
        crondescribe = request.POST.get("crondescribe", "")
        cronjobcmd = request.POST.get("jobcmd", "")
        cronmachines = request.POST.get("machines", "")
        run_user = request.POST.get("run_user", "")
        
        if not all((minute, hour, day, month, weekday, user, cronname, cronjobcmd, cronmachines, crondescribe)):
            return HttpResponse(json.dumps({
                "msg": "填写所有信息!",
                "code": "1"
            }), content_type="application/json")
        
        playbook_template = """---
- hosts: all
  gather_facts: false
  tasks:
    - name: Add crontab task
      cron:
        name: '{cronname}'
        minute: '{minute}'
        hour: '{hour}'
        day: '{day}'
        month: '{month}'
        weekday: '{weekday}'
        user: '{user}'
        job: '{jobcmd}'
    """.format(cronname=cronname, minute=minute, hour=hour, day=day, month=month, weekday=weekday, user=user,
               jobcmd=cronjobcmd)
        
        playbook_name = "crontabtask_{}".format(cronname)
        playbook_path = os.path.join(PLAYBOOK_BASE_PATH, playbook_name)
        with open(playbook_path, 'w') as f:
            f.write(playbook_template.strip("\n"))
            
        # 存储任务
        cron = CrontabTasks.objects.create(cron_name=cronname,
                                           cron_describe=crondescribe,
                                           cron_machines=cronmachines,
                                           task_status="1",
                                           playbook_name=playbook_name,
                                           playbook_content=playbook_template.strip("\n"),
                                           cron_schedule={"minute": minute,
                                                          "hour": hour,
                                                          "day": day,
                                                          "month": month,
                                                          "weekday": weekday},
                                           cmd=cronjobcmd,
                                           run_user=run_user,
                                           create_user=request.user.username,
                                           )
        cron.save()
        cron = CrontabTasks.objects.get(cron_name=cronname)
        id = cron.id
        # 异步执行
        r = execute_playbook.delay(playbook_path, cronmachines.split(','), id, task_type="cron", cron_action="add")
        # print(r.task_id, r.status)
        return HttpResponse(json.dumps({"msg": "任务: {}添加成功".format(cronname), "code": "0"}))


class CrontabDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = CrontabTasks
    template_name = 'scheduler/crontabtask_detail.html'
    page_title = '计划详情'
    context_object_name = 'task'


class CronCallBackView(View):
    def get(self, request, id):
        result = json.loads(request.body)
        result = json.loads(result)
        task_result = result['task_result']
        code = task_result['code']
        cron_action = request.GET.get("action")
        print(cron_action)
        
        # 根据action进行状态更新
        if cron_action == "add":
            if int(code) == 0:
                # 执行成功
                task_status = "2"
                
            elif int(code) > 1000:
                # 未执行(根据格式,playbook,host_list问题)
                task_status = "0"
                
            else:
                task_status = "3"
        elif cron_action == "delete":
            if int(code) == 0:
                # 执行成功,已删除
                task_status = "4"
    
        # 更新
        task = CrontabTasks.objects.filter(id=id).update(task_result=task_result, task_status=task_status)
        return HttpResponse(json.dumps({"msg": "task_id:{} callback succeed".format(id)}))

def host_run_result_cron(request):
    resp = {"msg": "", "code": "", "host_result": ""}
    host_result, msg, code = "", "", "0"
    taskid = request.GET.get("taskid")
    ip = request.GET.get("ip")

    # 从缓存或者数据库获取执行结果
    try:
        ansible_task = CrontabTasks.objects.get(id=taskid)
        host_result = ansible_task.task_result['all_host_detail_result'][ip]
    except Exception as e:
        msg = str(e)
        code = "1"

    finally:
        resp.update({
            "host_result": host_result,
            "code": code,
            "msg": msg
        })
        return HttpResponse(json.dumps(resp), content_type="application/json")
    
    
class DeleteCrontabView(LoginRequiredMixin, View):
    
    def get(self, request):
        id = request.GET.get("id")
        cron = CrontabTasks.objects.get(id=id)
        playbook_template = """---
- hosts: all
  gather_facts: false
  tasks:
    - name: Delete crontab task
      cron:
        name: {cronname}
        user: {user}
        state: absent
    """.format(cronname=cron.cron_name, user=cron.run_user)
        
        playbook_name = "crontabtask_{}_delete".format(cron.cron_name)
        playbook_path = os.path.join(PLAYBOOK_BASE_PATH, playbook_name)
        with open(playbook_path, 'w') as f:
            f.write(playbook_template.strip("\n"))
        
        r = execute_playbook.delay(playbook_path, cron.cron_machines.split(','), cron.id, task_type="cron",cron_action="delete")
        cron.task_status = "1"
        cron.save()
        
        return HttpResponse(json.dumps({"msg": "后台开始删除任务: {}".format(cron.cron_name), "code": "0"}))

