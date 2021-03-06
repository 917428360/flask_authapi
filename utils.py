#!/usr/bin/env python
#coding:utf-8

import configparser
import logging,logging.handlers
from flask import render_template, json, jsonify, request, abort, g,make_response
from functools import wraps

def get_config(service_conf, section=''):
    config = configparser.ConfigParser()
    config.read(service_conf)

    conf_items = dict(config.items('common')) if config.has_section('common') else {}
    if section and config.has_section(section):
       conf_items.update(config.items(section))
    return conf_items

def WriteLog(log_name):
    log_filename = "/api/api.log"
    log_level = logging.DEBUG
    format = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)2d]-%(funcName)s %(levelname)s %(message)s')
    handler = logging.handlers.RotatingFileHandler(log_filename, mode='a', maxBytes=10*1024*1024, backupCount=5)
    handler.setFormatter(format)

    logger = logging.getLogger(log_name)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    return logger         

def process_result(data, output):
    black = ["_sa_instance_state"]
    ret = []
    for obj in data:
        if output:
            tmp = {}
            for f in output:
                tmp[f] = getattr(obj, f)
            ret.append(tmp)
        else:
            tmp = obj.__dict__
            for p in black:
                try:
                    tmp.pop(p)
                except:
                    pass 
            ret.append(tmp)
    return ret

def stru_key_value(data):
    dic = {}
    for a in data: 
        dic.setdefault(a[0], []).append(a[1])
    return dic

def stru_data(data):
    a=[]
    for k in data:
        for key,value in k.items():
            a.append(value)
    return a            


def role_required(f):
    """权限查看"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        roles=[i.name for i in g.user.roles]
        #roles=['admin','user','cmdb']
        print(roles)
        if 'cmdb' in roles or 'admin' in roles: 
            return f(*args,**kwargs)
        return jsonify({'code':10003,'msg':'你没有权限'}) 
    return wrapper
