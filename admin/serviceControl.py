#coding:utf8
"""
Created on 2013-8-12

@author: lan (www.9miao.com)
"""
from twisted.internet import reactor
from twisted.python import log

from globalobject import GlobalObject

reactor = reactor


def serverStop():
    log.msg('stop')
    if GlobalObject().stophandler:
        GlobalObject().stophandler()
    reactor.callLater(0.5,reactor.stop)
    return True

def sreload():
    log.msg('reload')
    if GlobalObject().reloadmodule:
        reload(GlobalObject().reloadmodule)
    return True



def initControl(service):
    service.mapTarget(serverStop)
    service.mapTarget(sreload)
