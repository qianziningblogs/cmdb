import os
import datetime
import json
from collections import namedtuple
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback import CallbackBase
from ansible.errors import AnsibleParserError

class MyCallBack(CallbackBase):
    # 这里是状态回调，各种成功失败的状态,里面的各种方法其实都是从写于CallbackBase父类里面的，其实还有很多，可以根据需要拿出来用
    def __init__(self,*args):
        super(MyCallBack,self).__init__(display=None)
        self.fail_list = []
        self.success_list = []
        self.unreachable_list = []
        self.all_host_detail_result = {}
        
    def v2_runner_on_ok(self,result):
        task_name = result.task_name
        host=result._host.get_name()
        if host not in self.all_host_detail_result.keys():
            self.all_host_detail_result.update({host: []})
            
        self.all_host_detail_result[host].append("task-{}: execute succeed.".format(task_name))
        
        
    def v2_runner_on_failed(self, result, ignore_errors=False):
        task_name = result.task_name
        host = result._host.get_name()
        
        if host not in self.all_host_detail_result.keys():
            self.all_host_detail_result.update({host: ""})
            
        if host not in self.fail_list:
            self.fail_list.append(host)
            
        if result._result['rc'] != 0:
            self.all_host_detail_result[host].append("task-{}: execute failed because of {}".format(
                task_name, result._result['stderr']))
            

    def v2_runner_on_unreachable(self, result):
        task_name = result.task_name
        host = result._host.get_name()
        print(task_name, host)
        if host not in self.all_host_detail_result.keys():
            self.all_host_detail_result.update({host: []})
            
        if host not in self.unreachable_list:
            self.unreachable_list.append(host)
        self.all_host_detail_result[host].append("task-{}: host unreachable".format(task_name))


class RunPlayBook(object):
    def __init__(self, playbook=None, extra_vars={},
            host_list=None,
            connection='ssh',
            become=False,
            become_user=None,
            module_path=None,
            fork=10,
            ansible_cfg=None,
            passwords={},
            check=False):
        self.playbook_path = playbook
        self.passwords = passwords
        self.extra_vars = extra_vars
        self.host_list = host_list
        Options = namedtuple('Options',['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path',
                    'forks', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                    'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check','diff'])
        self.options = Options(listtags=False, listtasks=False,listhosts=False, syntax=False,diff=False,
                connection=connection, module_path=module_path,
                forks=fork, private_key_file=None,
                ssh_common_args=None, ssh_extra_args=None,
                sftp_extra_args=None, scp_extra_args=None,
                become=become, become_method=None,
                become_user=become_user,
                verbosity=None, check=check
                )
        if ansible_cfg != None:
            os.environ['ANSIBLE_CONFIG'] = ansible_cfg
       
        # 动态生成 hosts
        self.loader = DataLoader()
        self.inventory = InventoryManager(loader=self.loader, sources=','.join(self.host_list)+',')
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

    # 定义 运行方法和返回值
    def run(self):
        code, msg = 0, ""
        
        if not self.host_list[0]:
            code = 1001
            msg = "主机列表不可用"
            run_results = {"code": str(code), "msg": msg}
            return run_results
            
        if not self.playbook_path  or not os.path.exists(self.playbook_path):
            code = 1002
            msg ='{} is not exist'.format(self.playbook_path)
            self.run_results = {"code": str(code), "msg": msg}
            return self.run_results
        
        pbex = PlaybookExecutor(playbooks=[self.playbook_path],
                    inventory=self.inventory,
                    variable_manager=self.variable_manager,
                    loader=self.loader,
                    options=self.options,
                    passwords=self.passwords)
        self.results_callback = MyCallBack()
        
        pbex._tqm._stdout_callback = self.results_callback
        try:
            """
                code == 4: 有不可达的机器
                code == 2: 有执行failed的任务
            """
            code = pbex.run()
            print("pbex.run.code:", code)
            msg = "{} execute finished, but some error occurred".format(self.playbook_path)
        except Exception as e:
            code = 1003
            err_msg = str(e)
            try:
                err_list = err_msg.split("\n")
                err_msg = err_list[0]
            except:
                pass
            msg = "{} execute failed because: {}".format(self.playbook_path.split('/')[-1], err_msg)
            
        run_results = {"code": code, "msg": msg}
        return run_results
            
        


    def fetch_result(self):
        run_result = self.run()
        code = run_result['code']
        msg = ""
        # 发生灾难性错误, yml格式, playbook路径错误...
        if code > 1000:
            return {"code": code, "msg": run_result['msg']}
        
        elif code == 2 or code == 4:
            msg = "执行过程中发生异常"

        elif code == 0:
            msg = "执行过程没有任何异常"
            
        for h in self.host_list:
            if h not in self.results_callback.fail_list and h not in self.results_callback.unreachable_list:
                self.results_callback.success_list.append(h)
        
        return {"success": self.results_callback.success_list,
                "failed": self.results_callback.fail_list,
                "unreachable": self.results_callback.unreachable_list,
                "code": code,
                "msg": msg,
                "all_host_detail_result": self.results_callback.all_host_detail_result
                }



if __name__ == '__main__':
    # task_run = RunPlayBook(playbook='/tmp/main.yml', host_list=["192.168.20.101"])
    task_run = RunPlayBook(playbook='/Users/Weelin/Desktop/a.yml', host_list=["192.168.20.101", "192.168.20.102"])
    run_result = task_run.fetch_result()
    if run_result['code'] != "0":
        print("output:", run_result['msg'])
    else:
        for k, v in run_result.items():
            if isinstance(v, dict):
                for subk, subv in v.items():
                    print(subk, subv)
            else:
                print(k, v)