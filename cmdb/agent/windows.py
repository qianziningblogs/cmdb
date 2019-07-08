#!/usr/bin/env python
# coding: utf-8
# @Time   : windows.py
# @Author : Derek
# @File   : 2018/4/3 16:23

import subprocess
import socket
import platform

class windows():
    def delNoneDate(self,data):
        return [x.strip() for x in data if x != ""]


    def get_hostname(self):
        os_out=subprocess.getoutput("wmic os get caption").split("\n")
        return {'hostname': socket.gethostname(),'os':platform.uname()[0],'os_version':self.delNoneDate(os_out)[1],'kelnel':platform.uname()[3]}


    def get_mem(self):
        mem = subprocess.getoutput('wmic memorychip get capacity,serialnumber,speed,manufacturer').split('\n')
        keys = ['size', 'vender', 'sn', 'speed']
        child_list = [dict(dict(zip(keys, [h for h in self.delNoneDate(i.split(" "))])), **{'type': ''}) for i in
                      self.delNoneDate(mem)[1:]]
        return {'mem': {"child": child_list}}


    def get_network(self):
        network = subprocess.getoutput("wmic nicconfig get ipaddress,ipsubnet,macaddress,servicename").split("\n")
        network = self.delNoneDate(network)
        child_list=[]
        for n in network[1:]:
            n = self.delNoneDate(n.split(" "))
            if len(n) < 2:
                continue
            else:
                values=['mac','dev'] if len(n)==2 else ['ipv4','ipv6','ipv4_netmask','ipv6_netmask','mac','dev']
                child_list.append(dict(zip(values,[m.replace('{"',"").replace('"}',"").replace('",',"").replace('"',"") for m in n])))
        return {'network':{'child':child_list}}


    def get_os(self):
        vender=subprocess.getoutput("wmic computersystem get manufacturer").split("\n")
        prodctname=subprocess.getoutput("wmic computersystem get model").split("\n")
        sn=subprocess.getoutput('wmic bios get serialnumber').split('\n')
        return {'system': {'vender':self.delNoneDate(vender)[1], 'productname': self.delNoneDate(prodctname)[1],'sn':self.delNoneDate(sn)[1:][0]}}


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
        return {'cpu':cpu}


    def get_bios(self):
        bios = {}
        version = subprocess.getoutput('wmic bios get SMBIOSBIOSVersion').split('\n')
        bios['Version'] = self.delNoneDate(version)[1]
        vendor = subprocess.getoutput('wmic bios get Manufacturer').split('\n')
        bios['Vendor'] = self.delNoneDate(vendor)[1]
        return {'bios': bios}

h=windows()
all={}
all.update(h.get_hostname())
all.update(h.get_mem())
all.update(h.get_network())
all.update(h.get_os())
all.update(h.get_cpu())
all.update(h.get_bios())
print(all)