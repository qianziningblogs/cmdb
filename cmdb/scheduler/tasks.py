import requests
import json
from scheduler.utils.ansibleapi import RunPlayBook
from cmdb.celery import app as celery_app
from django.conf import settings

@celery_app.task(bind=True, queue='cmdb')
def execute_playbook(self, playbook_filepath, host_list, id, task_type="ansible", cron_action="add"):
    task_run = RunPlayBook(playbook=playbook_filepath, host_list=host_list,
                           extra_vars={},
                           connection='ssh',
                           become=False,
                           become_user=None,
                           module_path=None,
                           fork=10,
                           ansible_cfg=None,
                           passwords={},
                           check=False)
    run_result = task_run.fetch_result()
    data = {"task_result": run_result}
    if task_type == "ansible":
        resp = requests.get("http://{}/scheduler/ansibletask/callback/{}/".format(settings.CMDB_DOMAIN, id),
                            json = json.dumps(data))
        
    elif task_type == "cron" and cron_action == "add":
        resp = requests.get("http://{}/scheduler/crontabtask/callback/{}/?action={}".format(settings.CMDB_DOMAIN, id,
                                                                                            cron_action),json=json.dumps(data))
    elif task_type == "cron" and cron_action == "delete":
        resp = requests.get("http://{}/scheduler/crontabtask/callback/{}/?action={}".format(settings.CMDB_DOMAIN, id,
                                                                                          cron_action),json=json.dumps(data))
    return run_result
    



if __name__ == "__main__":
    r = execute_playbook(playbook_filepath='/tmp/main.yml', host_list=["192.168.20.101"], id='4')
    print(r)