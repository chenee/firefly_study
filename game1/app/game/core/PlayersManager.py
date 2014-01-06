#coding:utf8
"""
Created on 2011-3-24

@author: sean_lan
"""
from singleton import Singleton

class PlayersManager:
    """在线角色单例管理器"""

    __metaclass__ = Singleton

    def __init__(self):
        """初始化单例管理器"""
        self._players = {}
    
    def getAll(self):
        alllist=self._players.values()
        return alllist
    
    def addPlayer(self, player):
        """添加一个在线角色"""
        if self._players.has_key(player.baseInfo.id):
#            raise Exception("系统记录冲突")
            pass
        self._players[player.baseInfo.id] = player

    def getPlayerByID(self, pid):
        """根据角色id获取玩家角色实例
        @id （int） 角色id
        """
        return self._players.get(pid,None)

    
    def getPlayerBydynamicId(self,dynamicId):
        """根据角色动态id获取玩家角色实例
        @dynamicId （int） 角色动态id
        """
        for player in self._players.values():
            if player.dynamicId ==dynamicId:
                return player
        return None

    def getPlayerByNickname(self, nickname):
        """根据角色昵称获取玩家角色实例
        @nickname （str） 角色昵称
        """
        for k in self._players.values():
            if k.baseInfo.getNickName() == nickname:
                return k
        return None

    def dropPlayer(self, player):
        """移除在线角色
        @player （PlayerCharacter）角色实例
        """
        playerId = player.baseInfo.id
        self.dropPlayerByID(playerId)

    def dropPlayerByID(self, pid):
        """移除在线角色
        @id （int） 角色id
        """
        try:
            del self._players[pid]
        except:
            pass
        
    def IsPlayerOnline(self,pid):
        """判断角色是否在线"""
        return self._players.has_key(pid)
    
    def doPlayerOffLine(self,player):
        """
        """
        pass
    
    
    
