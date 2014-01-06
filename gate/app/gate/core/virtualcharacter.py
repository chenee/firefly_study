#coding:utf8
"""
Created on 2012-3-5
虚拟角色类，只是记录角色当前所在的节点
@author: sean_lan
"""
class VirtualCharacter:
    """虚拟角色类"""

    def __init__(self,characterId,dynamicId,node=201000):
        """初始化
        @param characterId: int 角色的id
        @param dynamicId: int 角色的客户端ID
        @param node: int 角色所在节点服务的id
        @param locked: bool 角色的锁定状态
        """
        self.characterId = characterId
        self.dynamicId = dynamicId
        self.node = node
        self.locked = False
        self.famId = 0

    def getLocked(self):
        """获取角色的锁定状态"""
        return self.locked

    def lock(self):
        """锁定角色节点"""
        self.locked = True

    def release(self):
        """释放锁定状态"""
        self.locked = False

    def getCharacterId(self):
        """获取角色的ID
        """
        return self.characterId

    def getDynamicId(self):
        """获取角色的动态ID"""
        return self.dynamicId

    def setDynamicId(self,dynamicId):
        """设置动态ID"""
        self.dynamicId = dynamicId

    def getNode(self):
        """返回角色所在的节点服务ID"""
        return self.node

    def setNode(self,node):
        """设置角色的节点服务ID
        @param node: int 节点的id
        """
        self.node = node

    def setFamId(self,famId):
        """设置副本的id"""
        self.famId = famId

    def getFamId(self):
        """获取副本的id
        """
        return self.famId







