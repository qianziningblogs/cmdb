#!/usr/bin/env python
# coding: utf-8 
# @Time   : test.py
# @Author : Derek
# @File   : 2018/4/2 11:16
#!/usr/bin/env python
#encoding: utf-8

from subprocess import Popen, PIPE
import socket



def parserData(data):
    lines_list = data.split(b'\n')
    info_list = []
    for index, line in enumerate(lines_list):
        if index == 0 :
             tmp_l = []
             tmp_l.append(line)
        else:
            if len(line) != 0:
                tmp_l.append(line)
            elif index < len(lines_list) - 1:
                info_list.append(tmp_l)
                tmp_l = []
    return info_list


def getIfconfigInfo():
    '''
    根据 ifconfig 命令获取网络设备信息
    {
        "dev": (ip, mac, netmask),
        ...
    }
    '''
    interface_info_dict = {}
    p = Popen(['ifconfig'], stdout = PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        return

    interface_info_list = parserData(stdout)
    for info in interface_info_list:
        ip, dev, mac, netmask = info[1].split()[1], info[0].split(':')[0], info[2].split()[1], info[1].split()[3]
        interface_info_dict[dev] = dict([("ip", ip), ("mac", mac), ("netmask", netmask)])
    return interface_info_dict

def dev_ip_mac():
    d = getIfconfigInfo()
    if not d:
        return
    for dev,(ip,mac, netmask) in d.items():
        print(dev, ip, mac, netmask)



''' 获取 dmidecode 命令的输出 '''
def getDmi():
    p = Popen(['dmidecode'], stdout = PIPE)
    stdout, stderr = p.communicate()
    if stderr:
        return
    return stdout


''' 根据输入的dmi段落数据 分析出指定参数 '''
def parseDmi():
    '''
       {'vender': 'VMware, Inc.', 'product': 'VMware Virtual Platform', 'sn': 'VMware-56 4d 97 80 04 3a e5 55-29 7c b3 3b 61 04 27 e1'}
    '''
    dic = {}
    parsed_data = parserData(getDmi())
    parsed_data = [i for i in parsed_data if i[1].startswith('System Information')]
    parsed_data = parsed_data[0][2:]
    dmi_dic = dict([i.strip().split(':') for i in parsed_data])
    dic['vender'] = dmi_dic['Manufacturer'].strip()
    dic['product'] = dmi_dic['Product Name'].strip()
    dic['sn'] = dmi_dic['Serial Number'].strip()
    return dic

def firm_info():
    for k, v in parseDmi().items():
        print(k, v)


''' 获取Linux系统主机名称'''
def getHostname():
    try:
        hostname = socket.getfqdn(socket.gethostname())
    except:
        hostname = 'undefined'
    return {'hostname':hostname}


''' 获取Linux系统的版本信息 '''
def getOsVersion():
    with open('/etc/issue') as fd:
        for line in fd:
            osver = line.strip()
            break
    return {'osver':osver}

''' 获取CPU的型号和CPU的核心数 '''
def getCpu():
    num = 0
    with open('/proc/cpuinfo') as fd:
        for line in fd:
            if line.startswith('processor'):
                num += 1
            if line.startswith('model name'):
                cpu_model = line.split(':')[1].strip().split()
                cpu_model = cpu_model[0] + ' ' + cpu_model[2]  + ' ' + cpu_model[-1]
    return {'cpu_num':num, 'cpu_model':cpu_model}

''' 获取Linux系统的总物理内存 '''
def getMemory():
    with open('/proc/meminfo') as fd:
        for line in fd:
            if line.startswith('MemTotal'):
                mem = int(line.split()[1].strip())
                break
    mem = '%.f' % (mem / 1024.0) + ' MB'
    return {'Memory':mem}



def debug():
    print('获取dev,ip,mac,netmask'.center(60, '='))
    dev_ip_mac()

    print('获取硬件信息sn vender product'.center(60, '='))
    firm_info()

    print('获取主机名,hostname'.center(60, '='))
    print(getHostname().get('hostname'))

    print('获取cpu信息'.center(60, '='))
    print(getCpu())

    print('获取mem信息'.center(60, '='))
    print(getMemory())


if __name__ == "__main__":
    #debug()

    host_info = {}

    host_info.update(getIfconfigInfo())
    host_info.update(parseDmi())
    host_info.update(getCpu())
    host_info.update(getMemory())
    print(host_info)