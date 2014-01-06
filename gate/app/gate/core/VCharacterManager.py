#coding:utf8
"""
Created on 2012-3-2

@author: sean_lan
"""
from singleton import Singleton

class VCharacterManager:
    """角色管理器"""

    __metaclass__ = Singleton

    def __init__(self):
        """记录角色ID与客户端id的关系"""
        self.character_client = {}
        self.client_character = {}

    def addVCharacter(self,vcharacter):
        """添加一个角色的
        @param vcharacter: VirtualCharacter Object
        """
        characterId = vcharacter.getCharacterId()
        self.character_client[characterId] = vcharacter

    def getVCharacterByClientId(self,clientId):
        """根据客户端ID获取虚拟角色
        @param clientId: int 客户端的id
        """
        for vcharacter in self.character_client.values():
            if vcharacter.getDynamicId() == clientId:
                return vcharacter
        return None

    def getVCharacterByCharacterId(self,characterId):
        """根据角色的ID获取角色"""
        vcharacter = self.character_client.get(characterId)
        return vcharacter

    def dropVCharacterByClientId(self,clientId):
        """删除角色
        @param clientId: int 客户端的动态ID
        """
        try:
            vcharacter = self.getVCharacterByClientId(clientId)
            if vcharacter:
                characterId = vcharacter.getCharacterId()
                del self.character_client[characterId]
            else:
                pass
        finally:
            pass

    def dropVCharacterByCharacterId(self,characterId):
        """删除角色
        @param clientId: int 客户端的动态ID
        """
        try:
            del self.character_client[characterId]
        finally:
            pass

    def getNodeByClientId(self,dynamicId):
        """根据客户端的ID获取服务节点的id
        @param dynamicId: int 客户端的id
        """
        vcharacter = self.getVCharacterByClientId(dynamicId)
        if vcharacter:
            return vcharacter.getNode()
        return -1

    def getNodeByCharacterId(self,characterId):
        """根据角色的ID获取服务节点的ID
        @param characterId: int 角色的ID
        """
        vcharacter = self.character_client.get(characterId)
        if vcharacter:
            return vcharacter.getNode()
        return -1

    def getClientIdByCharacterId(self,characterId):
        """根据角色的ID获取客户端的ID
        @param characterId: int 角色的ID
        """
        vcharacter = self.character_client.get(characterId)
        if vcharacter:
            return vcharacter.getDynamicId()
        return -1

    def getCharacterIdByClientId(self,dynamicId):
        """根据客户端的ID获取角色的ID
        @param characterId: int 角色的ID
        """
        vcharacter = self.getVCharacterByClientId(dynamicId)
        if vcharacter:
            return vcharacter.getCharacterId()
        return -1


