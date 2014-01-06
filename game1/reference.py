#coding:utf8
"""
Created on 2011-10-14

@author: lan (www.9miao.com)
"""
from twisted.spread import pb


class ProxyReference(pb.Referenceable):
    """代理通道"""

    def __init__(self,parent):
        """初始化"""
        pb.Referenceable()
        self._parent = parent

    def remote_callChild(self, command,*arg,**kw): #change to remote_callLeafNode
        """代理发送数据
        """
        return self._parent.callTarget(command,*arg,**kw)




