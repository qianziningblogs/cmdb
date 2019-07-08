import json
import os
import datetime
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import AnsibleTasks
from servers.models import Host
from utils.mixin import CommonMixin
from .tasks import execute_playbook
import logging

# logger_cmdb = logging.getLogger('django')
PLAYBOOK_BASE_PATH = os.path.join("/tmp/",'playbook')
if not os.path.exists(PLAYBOOK_BASE_PATH):
    os.mkdir(PLAYBOOK_BASE_PATH)
    
class AnsibleTasksList(LoginRequiredMixin, CommonMixin, ListView):
    module = AnsibleTasks
    template_name = 'scheduler/ansibletask_list.html'
    paginate_by = '15'
    context_object_name = 'tasks'
    page_title = '任务列表'
    
    def get_queryset(self):
        tasks = AnsibleTasks.objects.all()
        
        task_name = self.request.GET.get("task_name", "")
        if task_name:
            tasks = tasks.filter(task_name__icontains=task_name)
        task_status = self.request.GET.get("task_status", "")
        if task_status:
            tasks = tasks.filter(task_status=task_status)
        return tasks


class AnsibleCreateView(LoginRequiredMixin, CommonMixin, View):
    def get(self, request):
        page_title = '任务创建'
        machines = Host.objects.all()
        return render(request, "scheduler/ansibletask_create.html", {"html": "<em><b>脚本预览......</b></em>",
                                                                     "page_title": page_title,
                                                                     "machines": machines})
    
    def post(self, request):
        task_name = request.POST.get("task_name", '').strip()
        task_describe = request.POST.get("task_describe", '').strip()
        task_machines = request.POST.get("task_machines", '').strip()
        print(task_machines, task_describe, task_name)
        resp = {"code": "0", "msg": "基本信息添加成功"}
        if not task_describe or not task_name or not task_machines:
            resp['code'] = "1"
            resp['msg'] = "正确填写信息"
        
        response = HttpResponse(json.dumps(resp), content_type="application/json")
        response.set_cookie("task_name", task_name)
        response.set_cookie("task_describe", task_describe)
        response.set_cookie("task_machines", task_machines)
        return response


def upload_playbook(request):
    resp = {"code": "1",
            "msg": "没有正确上传脚本"}
    
    try:
        html = ""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        filename = "{}_{}".format(request.FILES['file'].name, timestamp)
        filepath = os.path.join(PLAYBOOK_BASE_PATH, filename)
        if request.method == "POST":
            with open(filepath, 'w') as f:
                for chunk in request.FILES['file'].chunks():
                    chunk = str(chunk, encoding='utf-8')
                    # 写入文件做记录
                    f.write(chunk)
                    html += chunk
            resp.update({"code": "0",
                         "msg": "success",
                         "html": html})
            response = HttpResponse(json.dumps(resp), content_type="application/json")
            response.set_cookie("playbook_name", filename)
            return response
    except Exception as e:
        resp.update({"html": "<span>剧本加载失败(.yml or .yaml):{}</span>".format(str(e))})
    
    return HttpResponse(json.dumps(resp), content_type="application/json")


def ansible_task_save_and_execute(request):
    filename = request.COOKIES["playbook_name"]
    task_name = request.COOKIES['task_name']
    task_describe = request.COOKIES['task_describe']
    task_machines = request.COOKIES['task_machines']
    create_user = request.user
    
    playbook_filepath = os.path.join(PLAYBOOK_BASE_PATH, "{}".format(filename))

    with open(playbook_filepath, "r") as f:
        playbook_content = f.read().strip()
    
    is_exists = AnsibleTasks.objects.filter(task_name=task_name).exists()
    if not is_exists:
        task = AnsibleTasks(task_name=task_name, playbook_name=filename, task_describe=task_describe,
                            task_machines=task_machines, create_user=create_user, playbook_content=playbook_content)
        
        task.save()
        task = AnsibleTasks.objects.get(task_name=task_name)
        # 生成host_list
        host_list = task_machines.split(',')
        try:
            r = execute_playbook.delay(playbook_filepath, host_list, id=task.id)
            # print(r)
            task.task_status = "1"
            task.save()
        except Exception as e:
            task.task_result = str(e)
            print(str(e))
            return HttpResponse(json.dumps({"msg": "任务未启动,{}".format(str(e)),
                                            "code": "1"}))
        
        return HttpResponse(json.dumps({"msg": "任务开始运行",
                                        "code": "0"}))
    
    return HttpResponse(json.dumps({"msg": "task_name: '{}' exists...".format(task_name),
                                    "code": "1"}))


class TaskCallBackView(View):
    def get(self, request, id):
        result = json.loads(request.body)
        result = json.loads(result)
        task_result = result['task_result']
        code = task_result['code']
        print(task_result)
        # 执行失败
        
        
        if int(code) == 0:
            # 执行成功
            task_status = "2"
            
        elif int(code) > 1000:
            # 未执行(根据格式,playbook,host_list问题)
            task_status = "0"
        else:
            # 执行失败
            task_status = "3"
        # 更新
        task = AnsibleTasks.objects.filter(id=id).update(task_result=task_result, task_status=task_status)
        
        return HttpResponse(json.dumps({"msg": "task_id:{} callback succeed".format(id)}))

class AnsibleTaskDetailView(LoginRequiredMixin, CommonMixin, DetailView):
    model = AnsibleTasks
    context_object_name = "task"
    pk_url_kwarg = 'pk'
    page_title = "任务详情"
    template_name = "scheduler/ansibletask_detail.html"




def ansibletask_status(request):
    
    ansibletaskmanager = AnsibleTasks.objects
    resp = {"waitting": ansibletaskmanager.filter(task_status="0").count(),
            "running": ansibletaskmanager.filter(task_status="1").count(),
            "finished": ansibletaskmanager.filter(task_status="2").count(),
            "failed": ansibletaskmanager.filter(task_status="3").count()
           }
    return HttpResponse(json.dumps(resp), content_type="application/json")

def host_run_result_ansible(request):
    resp = {"msg": "", "code": "", "host_result":""}
    host_result, msg, code = "", "", "0"
    taskid = request.GET.get("taskid")
    ip = request.GET.get("ip")
    
    # 从缓存或者数据库获取执行结果
    try:
        ansible_task = AnsibleTasks.objects.get(id=taskid)
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