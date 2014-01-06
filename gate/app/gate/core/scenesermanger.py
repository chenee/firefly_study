#coding:utf8
"""
Created on 2012-3-19
场景服务器管理者
@author: Administrator
"""
from singleton import Singleton
from twisted.python import log
from globalobject import GlobalObject


UP = 20  #每个场景服承载的角色上限

class  SceneSer:

    def __init__(self,sceneId):
        self.id = sceneId
        self._clients = set()

    def addClient(self,clientId):
        """添加一个客户端到场景服务器"""
        self._clients.add(clientId)

    def dropClient(self,clientId):
        """移除一个客户端"""
        self._clients.remove(clientId)

    def getClientCnt(self):
        """获取场景中的客户端数量"""
        return len(self._clients)

class SceneSerManager:

    __metaclass__ = Singleton

    def __init__(self):
        """初始化"""
        self._scenesers = {}
        self.initSceneSers()

    def initSceneSers(self):
        for childname in GlobalObject().root.childsmanager._childs.keys():
            if "game" in childname:
                self.addSceneSer(childname)

    def addSceneSer(self,sceneId):
        """添加一个场景服务器"""
        sceneser = SceneSer(sceneId)
        self._scenesers[sceneser.id] = sceneser
        return sceneser


    def getSceneServerById(self,sceneId):
        """返回场景服务的实例"""
        sceneser = self._scenesers.get(sceneId)
        if not sceneser:
            sceneser = self.addSceneSer(sceneId)
        return sceneser

    def addClient(self,sceneId,clientId):
        """添加一个客户端"""
        sceneser = self.getSceneServerById(sceneId)
        if not sceneser:
            return False
        sceneser.addClient(clientId)
        return True

    def dropClient(self,sceneId,clientId):
        """清除一个客户端"""
        sceneser = self.getSceneServerById(sceneId)
        if sceneser:
            try:
                sceneser.dropClient(clientId)
            except Exception:
                msg = "sceneId:%d-------clientId:%d"%(sceneId,clientId)
                log.err(msg)

    def getAllClientCnt(self):
        """获取公共场景中所有的客户端数量"""
        return sum([ser.getClientCnt() for ser in self._scenesers])


    def getBsetScenNodeId(self):
        """获取最佳的game服务器
        """
        serverlist = self._scenesers.values()
        slist = sorted(serverlist, reverse=False, key=lambda sser : sser.getClientCnt())
        if slist:
            return slist[0].id


