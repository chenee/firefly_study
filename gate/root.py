#coding:utf8
"""
Created on 2011-10-14
分布式根节点
@author: lan (www.9miao.com)
"""
from twisted.python import log
from twisted.spread import pb

from childmanager import ChildsManager
import services


class BilateralBroker(pb.Broker):

    def connectionLost(self, reason):
        clientID = self.transport.sessionno
        log.msg("node [%d] lose"%clientID)
        self.factory.root.childsmanager.dropChildByID(clientID)
        pb.Broker.connectionLost(self, reason)

class BilateralFactory(pb.PBServerFactory):

    protocol = BilateralBroker


class PBRoot(pb.Root):
    """PB 协议"""

    def __init__(self,serviceName,childManager = ChildsManager()):
        """初始化根节点
        """
        pb.Root()

        self.service = services.Service(serviceName)
        self.childsmanager = childManager

    def addServiceChannel(self,service):
        """添加服务通道
        @param service: Service Object(In bilateral.services)
        """
        self.service = service

    def remote_register(self,name,peer):
        """设置代理通道
        @param addr: (hostname,port)hostname 根节点的主机名,根节点的端口
        """
        log.msg('node [%s] registered' % name)
        self.childsmanager.addChildByNamePeer(name,peer)

    def remote_callTarget(self,command,*args,**kw):
        """远程调用方法
        @param commandId: int 指令号
        @param data: str 调用参数
        """
        data = self.service.callTarget(command,*args,**kw)
        return data

    def dropChild(self,*args,**kw):
        """删除子节点记录"""
        self.childsmanager.dropChild(*args,**kw)

    def dropChildByID(self,childId):
        """删除子节点记录"""
        self.childsmanager.dropChildByID(childId)

    def callChild(self,nodeID,*args,**kw):
        """调用子节点的接口
        @param nodeID: int 子节点的id
        return Defered Object
        """
        return self.childsmanager.callChild(nodeID,*args,**kw)

    def callChildByName(self,childname,*args,**kw):
        """调用子节点的接口
        @param childId: int 子节点的id
        return Defered Object
        """
        return self.childsmanager.callChildByName(childname,*args,**kw)

