"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from .ansibletask import (AnsibleCreateView,
                    upload_playbook,
                    ansible_task_save_and_execute,
                    TaskCallBackView,
                    AnsibleTasksList,
                    AnsibleTaskDetailView,
                    ansibletask_status,
                    host_run_result_ansible,
                    )

from .crontask import (
                        CronCreateView,
                        CronTasksList,
                        CrontabDetailView,
                        CronCallBackView,
                        DeleteCrontabView,
                        host_run_result_cron,
)

urlpatterns = [
    url(r'^ansibletask/create/$', AnsibleCreateView.as_view(), name="ansible_create"),
    url(r'^playbook/render/$', upload_playbook, name="upload"),
    url(r'^ansibletask/save/$', ansible_task_save_and_execute, name="ansible_save"),
    url(r'^ansibletask/callback/(?P<id>\d+)/$', TaskCallBackView.as_view(), name="ansible_callback"),
    url(r'^ansibletask/list/$', AnsibleTasksList.as_view(), name="ansible_list"),
    url(r'^ansibletask/detail/(?P<pk>\d+)/$', AnsibleTaskDetailView.as_view(), name="ansible_detail"),
    url(r'^ansibletask/status/sumary/$', ansibletask_status, name="ansibletask_status"),
    url(r'^ansibletask/host/result/$', host_run_result_ansible,name="host_result_ansible"),
    url(r'^crontabtask/create/$', CronCreateView.as_view(), name="crontabtask_create"),
    url(r'^crontabtask/list/$', CronTasksList.as_view(), name="crontabtask_list"),
    url(r'^crontabtask/detail/(?P<pk>\d+)/$', CrontabDetailView.as_view(), name="crontab_detail"),
    url(r'^crontabtask/callback/(?P<id>\d+)/$', CronCallBackView.as_view(), name="crontab_callback"),
    url(r'^crontabtask/host/result/$', host_run_result_cron, name="host_result_cron"),
    url(r'^crontabtask/delete/$', DeleteCrontabView.as_view(), name="crontab_delete"),

]
