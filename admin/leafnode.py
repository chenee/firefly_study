#coding:utf8
"""
Created on 2011-10-14

@author: lan (www.9miao.com)
"""
from twisted.spread import pb
from twisted.internet import reactor

reactor = reactor

from reference import ProxyReference
from services import Service

def callBack(obj,funcName,*args,**kw):
    """远程调用
    @param funcName: str 远程方法
    """
    return obj.callRemote(funcName, *args,**kw)


class leafNode(object):
    """远程调用对象"""

    def __init__(self,name):
        """初始化远程调用对象
        @param port: int 远程分布服的端口号
        @param rootaddr: 根节点服务器地址
        """
        self._name = name
        self._factory = pb.PBClientFactory()
        self._reference = ProxyReference(self)
        self._service = Service('proxy')

        self._addr = None

    def setName(self,name):
        """设置节点的名称"""
        self._name = name

    def getName(self):
        """获取节点的名称"""
        return self._name

    def connect(self,addr):
        """初始化远程调用对象"""
        self._addr = addr
        reactor.connectTCP(addr[0], addr[1], self._factory)
        self.register()

    def reconnect(self):
        """重新连接"""
        self.connect(self._addr)

    def addServiceChannel(self,service):
        """设置引用对象"""
        self._service = service

    def getServiceChannel(self):
        return self._service

    def register(self):
        """把本节点注册到RootNode,并且向RootNode发送代理通道对象
        """
        deferedRemote = self._factory.getRootObject()
        deferedRemote.addCallback(callBack, 'register', self._name, self._reference)

    def callRemote(self,commandId,*args,**kw):
        """远程调用"""
        deferedRemote = self._factory.getRootObject()
        return deferedRemote.addCallback(callBack,'callTarget',commandId,*args,**kw)

    def callTarget(self, targetKey, *args, **kw):
        self._service.callTarget(targetKey,*args,**kw)

