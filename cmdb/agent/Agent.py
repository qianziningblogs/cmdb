#encoding:utf8
from subprocess import Popen, PIPE
import subprocess
import socket
import datetime
import platform
import json
try:
    import wmi
except:
    pass

AUTO_REPORT_URL = "http://192.168.20.36:8000/auto/autoreport/{}/"
class Base(object):
    @classmethod
    def run_cmd(cls, cmd_list):
        '''
            ['dmidecode', '-t', 'memory']
        '''
        p = Popen(cmd_list, stdout=PIPE)
        stdout, stderr = p.communicate()
        if stderr:
            return
        return stdout

    @classmethod
    def parse_data(cls, ori_data):
        lines_list = ori_data.split('\n')
        group_list = []
        for index, line in enumerate(lines_list):
            if index == 0:
                tmp_l = []
                tmp_l.append(line)
            else:
                if len(line) != 0:
                    tmp_l.append(line)
                elif index == len(lines_list) - 1:
                    group_list.append(tmp_l)
                else:
                    group_list.append(tmp_l)
                    tmp_l = []
        return group_list

    @classmethod
    def change_maskint(cls, mask_int):
        mask_int = int(mask_int)
        bin_arr = ['0' for i in range(32)]
        for i in range(mask_int):
            bin_arr[i] = '1'
            tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
            tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
        return '.'.join(tmpmask)


class Memory(Base):
    @classmethod
    def mem_info(cls):
        mem_info = {"mem": {"child": []}}
        cmd_list = ['dmidecode', '-t', 'memory']
        ori_data = cls.run_cmd(cmd_list)
        group_list = cls.parse_data(ori_data)
        group_list = (group for group in group_list if "Memory Device" in group)

        for group in group_list:
            tmp_dict = {"size": "", "type": "", "speed": "", "vender": "", "sn": ""}
            ignore = False
            for line in group:
                if line.strip().split(':')[0] == 'Size':
                    tmp_dict["size"] = line.strip().split(':')[1].strip()
                    if "N" in line.strip().split(':')[1]:
                        ignore = True

                elif line.strip().split(':')[0] == 'Type':
                    tmp_dict["type"] = line.strip().split(':')[1].strip()

                elif line.strip().split(':')[0] == "Speed":
                    tmp_dict["speed"] = line.strip().split(':')[1].strip()

                elif line.strip().split(':')[0] == "Manufacturer":
                    tmp_dict["vender"] = line.strip().split(':')[1].strip()

                elif line.strip().split(':')[0] == "Serial Number":
                    tmp_dict["sn"] = line.strip().split(':')[1].strip()
            if not ignore:
                mem_info['mem']['child'].append(tmp_dict)

        return mem_info


class Net(Base):
    @classmethod
    def net_info(cls):
        net_info = {"network": {"child": []}}
        cmd_list = ['ip', 'addr']
        net_keys = ["dev", "mac", "ipv4", "ipv6", "ipv4_netmask", "ipv6_netmask"]
        with open('/proc/net/dev', 'r') as f:
            lines = f.read().strip().split('\n')[2:]
            devs = [line.split(':')[0].strip() for line in lines if line.split(':')[0].strip() != "lo"]
        dev_info_list = [dict.fromkeys(net_keys, "") for _ in devs]
        _ = [dev_info_list[index].update({"dev": dev}) for index, dev in enumerate(devs)]

        # get ip addr info
        ori_data = cls.run_cmd(cmd_list)
        lines = ori_data.split('\n')
        for index, line in enumerate(lines):
            for i, dev in enumerate(devs):
                if dev + ":" in line:
                    mac, ipv4, ipv6, ipv4_netmask, ipv6_netmask = "", "", "", "", ""
                    mac = lines[index + 1].split()[1]
                    ipv4, mask_int = lines[index + 2].split()[1].split("/") if "inet" in lines[index + 2] else ("", "")
                    # get ipv6
                    ipv6, ipv6_netmask = "", ""
                    sub_lines = lines[index + 2:]
                    for sub_index, sub_line in enumerate(sub_lines):
                        if "inet6" in sub_line.strip():
                            ipv6, ipv6_netmask = sub_lines[sub_index].split()[1].split("/")
                    ipv4_netmask = cls.change_maskint(mask_int) if ipv4 else ""
                    dev_info_list[i]['mac'] = mac
                    dev_info_list[i]['ipv4'] = ipv4
                    dev_info_list[i]['ipv6'] = ipv6
                    dev_info_list[i]['ipv4_netmask'] = ipv4_netmask
                    dev_info_list[i]['ipv6_netmask'] = ipv6_netmask

        net_info['network']['child'] = dev_info_list
        return net_info


class System(Base):
    @classmethod
    def system_info(cls):
        system_dict = {}
        cmd_list = ['dmidecode', '-t', 'system']
        ori_data = cls.run_cmd(cmd_list)
        group_list = cls.parse_data(ori_data)
        for group in group_list:
            if "Manufacture" in ''.join(group) and "Serial Number" in ''.join(group):
                for line in group:
                    if line.strip().split(':')[0] == "Manufacturer":
                        system_dict["vender"] = line.strip().split(':')[1].strip()
                    elif line.strip().split(':')[0] == "Product Name":
                        system_dict["productname"] = line.strip().split(':')[1].strip()
                    elif line.strip().split(':')[0] == "Serial Number":
                        system_dict["sn"] = line.strip().split(':')[1].strip()

        # 拿到hostname, kernel, os, os_version
        os_type = platform.system()
        if os_type.lower() == "linux":
            os, os_version, (hostname, kernel) = "linux", ' '.join(platform.linux_distribution()), platform.uname()[1:3]
            system_dict.update({"os": os, "os_version": os_version, "hostname": hostname, "kernel": kernel})
        return {"system": system_dict}


class Bios(Base):
    @classmethod
    def bios_info(cls):
        cmd_list = ['dmidecode', '-t', 'bios']
        ori_data = cls.run_cmd(cmd_list)
        group_list = cls.parse_data(ori_data)
        bios_dict = {}
        for group in group_list:
            if "Version" and "Vendor" in ''.join(group):
                for line in group:
                    if line.strip().split(':')[0] == "Vendor":
                        bios_dict["vender"] = line.strip().split(':')[1].strip()

                    elif line.strip().split(':')[0] == "Version":
                        bios_dict["version"] = line.strip().split(':')[1].strip()
                return {"bios": bios_dict}


class Cpu(Base):
    @classmethod
    def cpu_info(cls):
        count, modelname, cores, phyical, threads = "", "", "", "", ""
        cmd_list = ["lscpu"]
        with open('/proc/cpuinfo') as fd:
            # cpu model
            for line in fd:
                if line.startswith('model name'):
                    cpu_model = line.split(':')[1].strip().split()
                    cpu_model = cpu_model[0] + ' ' + cpu_model[2] + ' ' + cpu_model[-1]
                    break

        # count, cores_per_core,  phyical
        ori_data = cls.run_cmd(cmd_list)
        for line in ori_data.split('\n'):
            if "CPU(s)" == line.split(':')[0].strip():
                count = line.split(':')[1].strip()
            elif "Core(s) per socket" in line:
                cores = line.split(':')[1].strip()
            elif "Thread(s) per core" in line:
                threads = line.split(':')[1].strip()
        phyical = str(int(count) / int(cores) / int(threads))
        return {"cpu": {'count': count, 'modelname': cpu_model, "cores": cores, "phyical": phyical}}


class Disk(object):
    pass


class windows():

    def delNoneDate(self,data):
        return [x.strip() for x in data if x != ""]

    def get_hostname(self):
        os_out=subprocess.getoutput("wmic os get caption").split("\n")
        return {'hostname': socket.gethostname(),
                           'os':platform.uname()[0],
                           'os_version':self.delNoneDate(os_out)[1],
                           'kelnel':platform.uname()[3]
                }

    def get_mem(self):
        mem = subprocess.getoutput('wmic memorychip get capacity,serialnumber,speed,manufacturer').split('\n')
        keys = ['size', 'vender', 'sn', 'speed']
        child_list = [dict(dict(zip(keys, [h for h in self.delNoneDate(i.split(" "))])), **{'type': ''}) for i in
                      self.delNoneDate(mem)[1:]]
        return {'mem': {"child": child_list}}

    @property
    def get_network(self):
        child_list = []
        for nic in wmi.WMI().Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                item_data = {}
                item_data['mac'] = nic.MACAddress
                item_data['dev'] = nic.Caption
                if nic.IPAddress is not None:
                    item_data['ipv4'] = nic.IPAddress[0]
                    item_data['ipv4_netmask'] = nic.IPSubnet[0]
                    item_data['ipv6'] = nic.IPAddress[1]
                    item_data['ipv6_netmask'] = nic.IPSubnet[1]
                child_list.append(item_data)
        return {'network': {'child': child_list}}

    def get_os(self):
        vender = subprocess.getoutput("wmic computersystem get manufacturer").split("\n")
        prodctname = subprocess.getoutput("wmic computersystem get model").split("\n")
        sn = subprocess.getoutput('wmic bios get serialnumber').split('\n')

        system_info = {}
        system_info.update(self.get_hostname())
        system_info.update({'vender': self.delNoneDate(vender)[1],
                            'productname': self.delNoneDate(prodctname)[1],
                            'sn': self.delNoneDate(sn)[1:][0]})
        return {'system': system_info}

    def get_cpu(self):
        cpu = {}
        modelname = subprocess.getoutput('wmic cpu get name').split('\n')
        cpu['modelname'] = self.delNoneDate(modelname)[1]
        cpu_out = subprocess.getoutput('wmic cpu get NumberOfCores,NumberOfLogicalProcessors').split('\n')
        count_size = 0
        for i in self.delNoneDate(cpu_out)[1:]:
            count_size += int(self.delNoneDate(i.split(" "))[1])
            cpu['cores'] = i.split(" ")[0]
        cpu['phyical'] = str(len(self.delNoneDate(cpu_out)[1:]))
        cpu['count'] = str(count_size)
        return {'cpu': cpu}

    def get_bios(self):
        bios = {}
        version = subprocess.getoutput('wmic bios get SMBIOSBIOSVersion').split('\n')
        bios['Version'] = self.delNoneDate(version)[1]
        vendor = subprocess.getoutput('wmic bios get Manufacturer').split('\n')
        bios['Vendor'] = self.delNoneDate(vendor)[1]
        return {'bios': bios}


# 上报
def auto_report_by_urllib2(params, uuid_path):
    try:
        url = AUTO_REPORT_URL.format(list(params.keys())[0])
        request = urllib2.Request(url, data=json.dumps(params))
        response = urllib2.urlopen(request)
        r_json = json.loads(response.read())
        if r_json['code'] == "0":
            with open(uuid_path, 'w') as f:
                f.write(r_json['uuid'])
            msg = "{} auto report success...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
            return True, msg
        else:
            msg = "{} auto report failed,{}...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), r_json['msg'])
            return False, msg
    except Exception as e:
        msg = "{} auto report failed,{}...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), str(e))
        return False, msg


def auto_report_by_requests(params, uuid_path):
    try:
        url = AUTO_REPORT_URL.format(list(params.keys())[0])
        response = requests.post(url, data=json.dumps(params))
        r_json = response.json()
        if r_json['code'] == "0":
            with open(uuid_path, 'w') as f:
                f.write(r_json['uuid'])
                msg = "{} auto report success...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))
                return True, msg
        else:
            msg = "{} auto report failed,{}...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), r_json['msg'])
            return False, msg
    except Exception as e:
        msg = "{} auto report failed,{}...".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), str(e))
        return False, msg


if __name__ == "__main__":

    uuid, ip = "", ""
    value = {}
    uuid_path = "/etc/init.d/uuid" if platform.system().lower() == "linux" else "C:/uuid"
    try:
        with open(uuid_path, 'r') as f:
            uuid = f.read().strip()
    except:
        pass
        # uuid = "5db5b52a9a4d449f9396d38a8a3ec5c7"

    if platform.system().lower() == "linux":
        value.update(Memory.mem_info())
        value.update(Cpu.cpu_info())
        value.update(Net.net_info())
        value.update(System.system_info())
        value.update(Bios.bios_info())
        if not uuid:
            uuid = socket.gethostbyname(socket.gethostname())
        params = {uuid: value}

    elif platform.system().lower() == "windows":
        h = windows()
        value.update(h.get_mem())
        value.update(h.get_network)
        value.update(h.get_os())
        value.update(h.get_cpu())
        value.update(h.get_bios())
        if not uuid:
            uuid = socket.gethostbyname(socket.gethostname())
        params = {uuid: value}

    # 上报
    start_msg = "\n{} auto report begin...\n".format(datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))

    try:
        import requests
        result = auto_report_by_requests(params, uuid_path)
    except:
        import urllib2
        result = auto_report_by_urllib2(params, uuid_path)


    with open("agent.log", "a") as f:
        f.write(start_msg)
        f.write(result[1])