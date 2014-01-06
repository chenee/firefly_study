#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from twisted.python import log
from twisted.internet import defer

from services import CommandService
from globalobject import GlobalObject

class GateService(CommandService):

    def callTargetSingle(self,targetKey,*args,**kw):
        """call Target by Single
        @param conn: client connection
        @param targetKey: target ID
        @param data: client data
        """

        self._lock.acquire()
        try:
            target = self.getTarget(targetKey)
            if not target:
                log.err('localService: the command '+str(targetKey)+' not Found on service')
                return None
            if targetKey not in self.unDisplay:
                log.msg("localService: call method %s on service[single]"%target.__name__)

            defer_data = target(targetKey,*args,**kw)
            if not defer_data:
                return None
            if isinstance(defer_data,defer.Deferred):
                return defer_data
            d = defer.Deferred()
            d.callback(defer_data)
        finally:
            self._lock.release()
        return d

def initLocalService():
    localservice = GateService('localservice')
    GlobalObject().localservice = localservice

def addToLocalService(target):
    """服务处理
    @param target: func Object
    """
    GlobalObject().localservice.mapTarget(target)
