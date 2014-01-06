#coding:utf8
"""
Created on 2013-8-2

@author: lan (www.9miao.com)
"""
from twisted.python import log
from twisted.internet import reactor

from protoc import LiberateFactory
from leafnode import leafNode
from logobj import loogoo
from globalobject import GlobalObject
import services
import serviceControl
import os
import sys


reactor = reactor

def serverStop():
    log.msg('stop')
    if GlobalObject().stophandler:
        GlobalObject().stophandler()
    reactor.callLater(0.5,reactor.stop)
    return True

class NetServer:

    def __init__(self):
        """
        """
        self.netfactory = None#net前端
        # self.root = None#分布式root节点
        self.gates = {}#remote节点
        self.master_remote = None
        self.servername = None

    def config(self, config, dbconfig = None,memconfig = None,masterconf=None):
        """配置服务器
        """
        netport = config.get('netport')#客户端连接
        gatelist = config.get('remoteport',[])#remote节点配置列表
        servername = config.get('name')#服务器名称
        logpath = config.get('log')#日志
        app = config.get('app')#入口模块名称
        self.servername = servername

        if masterconf:
            masterport = masterconf.get('rootport')
            addr = ('localhost', masterport)
            leafnode = leafNode(servername)
            serviceControl.initControl(leafnode.getServiceChannel())
            leafnode.connect(addr)
            GlobalObject().leafNode = leafnode

        if netport:
            self.netfactory = LiberateFactory()
            netservice = services.CommandService("netservice")
            self.netfactory.addServiceChannel(netservice)
            reactor.listenTCP(netport, self.netfactory)
            GlobalObject().netfactory = self.netfactory

        for cnf in gatelist:
            rname = cnf.get('rootname')
            rport = cnf.get('rootport')
            self.gates[rname] = leafNode(servername)
            addr = ('localhost', rport)
            self.gates[rname].connect(addr)

        GlobalObject().remote = self.gates

        if logpath:
            log.addObserver(loogoo(logpath))  #日志处理
        log.startLogging(sys.stdout)

        if app:
            reactor.callLater(0.1, __import__, app)


    def start(self):
        """启动服务器
        """
        log.msg('%s start...' % self.servername)
        log.msg('%s pid: %s' % (self.servername, os.getpid()))
        reactor.run()


