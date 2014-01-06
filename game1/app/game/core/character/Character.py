#coding:utf8
"""
Created on 2011-3-23

@author: sean_lan
"""
from app.game.component.baseInfo.CharacterBaseInfoComponent import CharacterBaseInfoComponent



class Character(object):
    """角色通用类"""
    
    PLAYERTYPE = 1#玩家
    MONSTERTYPE = 2#怪物npc
    PETTYPE = 3#宠物
    MAXPOWER = 100#能量最大值
    
    def __init__(self, cid, name):
        """
               创建一个角色
        """
        self.baseInfo = CharacterBaseInfoComponent(self, cid, name)
        self.CharacterType = 0#角色的类型  1:玩家角色 2:怪物 3:宠物
        
    def setCharacterType(self,characterType):
        """设置角色类型"""
        self.CharacterType = characterType
        
    def getCharacterType(self):
        """获取角色类型
        """
        return self.CharacterType

    def getBaseID(self):
        return self.baseInfo.id
    
