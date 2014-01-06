#coding:utf8
"""
Created on 2013-8-2

@author: lan (www.9miao.com)
"""
import os
import sys

from twisted.python import log
from twisted.internet import reactor


from leafnode import leafNode
from dbpool import dbpool
from memclient import mclient

from logobj import loogoo
from globalobject import GlobalObject

reactor = reactor

def serverStop():
    log.msg('stop')
    if GlobalObject().stophandler:
        GlobalObject().stophandler()
    reactor.callLater(0.5,reactor.stop)
    return True

class DBServer:

    def __init__(self):
        """
        """
        self.leafNode = None
        self.db = None
        self.mem = None
        self.servername = None

    def config(self,config,dbconfig = None,memconfig = None,masterconf=None):
        """配置服务器
        """

        servername = config.get('name')#服务器名称
        logpath = config.get('log')#日志
        hasdb = config.get('db')#数据库连接
        hasmem = config.get('mem')#memcached连接

        app = config.get('app')#入口模块名称

        self.servername = servername

        if masterconf:
            masterport = masterconf.get('rootport')
            addr = ('localhost', masterport)
            self.leafNode = leafNode(servername)
            self.leafNode.connect(addr)
            GlobalObject().leafNode = self.leafNode


        if hasdb and dbconfig:
            log.msg(str(dbconfig))
            dbpool.initPool(**dbconfig)

        if hasmem and memconfig:
            urls = memconfig.get('urls')
            hostname = str(memconfig.get('hostname'))
            mclient.connect(urls, hostname)

        if logpath:
            log.addObserver(loogoo(logpath))#日志处理
        log.startLogging(sys.stdout)


        if app:
            reactor.callLater(0.1,__import__,app)


    def start(self):
        """启动服务器
        """
        log.msg('%s start...'%self.servername)
        log.msg('%s pid: %s'%(self.servername,os.getpid()))
        reactor.run()


