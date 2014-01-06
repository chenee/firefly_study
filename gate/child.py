#coding:utf8
"""
Created on 2011-10-14

@author: lan (www.9miao.com)
"""
class RemoteChild(object):
    """子节点对象"""

    def __init__(self,name,peer=None):
        """初始化子节点对象
        """
        self._name = name
        self._peer = peer

    def getName(self):
        """获取子节点的名称"""
        return self._name

    def setTransport(self,peer):
        """设置子节点的通道"""
        self._peer = peer

    def callbackChild(self, *args, **kw):
        """回调子节点的接口
        return a Defered Object (recvdata)

        game1:
        """
        recvdata = self._peer.callRemote('callChild', *args, **kw)
        return recvdata





