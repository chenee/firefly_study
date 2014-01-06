#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from globalobject import GlobalObject
from services import CommandService


remoteservice = CommandService("gateremote")
GlobalObject().remote["gate"].setServiceChannel(remoteservice)


def remoteserviceHandle(target):
    """
    """
    remoteservice.mapTarget(target)


