#!/usr/bin/python
# coding:utf-8
# author: rongjunfeng

import json
import subprocess
import psutil
import socket
import time
import re
import platform
import requests


headers = {'Content-Type': 'application/json'}
device_white = ['ens33','eth0']

def get_hostname():
    return socket.gethostname()

def get_device_info():
    ret = []
    for device, info in psutil.net_if_addrs().items():
        if device in device_white:
            device_info = {'device': device}
            for snic in info:
                if snic.family == 2:
                    device_info['ip'] = snic.address
                elif snic.family == 17:
                    device_info['mac'] = snic.address
            ret.append(device_info)
    return ret

def get_cpuinfo():
    ret = {"cpu": '', 'num': 0}
    with open('/proc/cpuinfo') as f:
        for line in f:
            line_list = line.strip().split(':')
            key = line_list[0].rstrip()
            if key == "model name":
                ret['cpu'] = line_list[1].lstrip()
            if key == "processor":
                ret['num'] += 1
    return ret

def get_disk():
    cmd = """/sbin/fdisk -l|grep Disk|egrep -v 'identifier|mapper|Disklabel'"""
    disk_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    partition_size = []
    for dev in disk_data.stdout.readlines():
        try:
            size = int(dev.strip().split(', ')[1].split()[0]) / 1024 / 1024 / 1024
            partition_size.append(str(size))
        except:
	        pass
    return " + ".join(partition_size)

def get_Manufacturer():
    cmd = """/usr/sbin/dmidecode | grep -A6 'System Information'"""
    ret = {}
    manufacturer_data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in manufacturer_data.stdout.readlines(500):
        line=str(line).strip('\n') 
        if "Manufacturer" in line:
            ret['manufacturers'] = line.split(': ')[1].strip('')
        elif "Product Name" in line:
            ret['manufacturers_type'] = line.split(': ')[1].strip('')
        elif "Serial Number" in line:
            ret['sn'] = line.split(': ')[1].strip('').replace(' ','')
        elif "UUID" in line:
            ret['uuid'] = line.split(': ')[1].strip('')
    return ret
    #return manufacturer_data.stdout.readline().split(': ')[1].strip()

# 出厂日期
def get_rel_date():
    cmd = """/usr/sbin/dmidecode | grep -i release"""
    data = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    date = str(data.stdout.readline(100)).split(': ')[1].strip()
    return re.sub(r'(\d+)/(\d+)/(\d+)',r'\3-\1-\2',date)  

def get_os_version():
    return " ".join(platform.linux_distribution())

def get_innerIp(ipinfo):
    inner_device = ["ens33"]
    ret = {}
    for info in ipinfo:
        if info.get('ip') and info.get('device', None) in inner_device:
            ret['ip'] = info['ip']
            ret['mac_address'] = info['mac']
            return  ret
    return {}

def get_Memtotal():
    with open('/proc/meminfo') as mem_open:
        a = int(mem_open.readline().split()[1])
        return a / 1024 
    

def run():
    data = {}
    data['hostname'] = get_hostname()
    data.update(get_innerIp(get_device_info()))
    cpuinfo = get_cpuinfo()
    data['cpu'] = "{cpu} {num}".format(**cpuinfo)
    data['disk'] = get_disk()
    data.update( get_Manufacturer())
    data['manufacture_date'] = get_rel_date()
    data['os'] = get_os_version()
    data['memory'] = get_Memtotal()
    if "VMware" in data['manufacturers']:
        data['vm_status'] = 0
    else:
        data['vm_status'] = 1 
    print(data)
    send(data)

def send(data): 
    payload = {"username":"admin","password":"123456"}
    r = requests.post("http://127.0.0.1:5000/devops/api/v1.0/login",headers=headers,data=json.dumps(payload))
    result_data=json.loads(r.text) 
    headers['token']=result_data['token']
    print(headers)
    url = "http://127.0.0.1:5000/devops/api/v1.0/server"
    r = requests.post(url,headers=headers,data=json.dumps(data))
    print(r.text)

if __name__ == "__main__":
    run()

