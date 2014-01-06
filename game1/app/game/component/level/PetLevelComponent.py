#coding:utf8
"""
Created on 2012-5-29
宠物等级
@author: Administrator
"""
from app.game.component.Component import Component
from app.share.dbopear import dbCharacterPet
from app.game.memmode import tbpetadmin

class PetLevelComponent(Component):
    """玩家等级组件类
    """
    MAXLEVEL = 100  #满级限制
    def __init__(self,owner,level = 1,exp = 0):
        """
        @param owner:  Character Object 组件拥有者
        @param level: int 宠物的等级
        @param exp:  int 宠物的当前经验
        """
        Component.__init__(self, owner)
        self._level = level
        self._exp = exp

    def getMaxExp(self):
        """计算当前级别的最大经验值"""
        maxExp = dbCharacterPet.PET_EXP.get(self._level,0)#400 + 60 * (self._level - 1) + 10 * self._level * (self._level + 1) * (self._level - 1)
        return int(maxExp)

    def getExp(self):
        """获取角色当前经验
        """
        return self._exp

    def setExp(self,exp):
        """设置角色当前经验值
        @param exp: int 经验值
        """
        self._exp = exp

    def updateExp(self,exp):
        """更新角色经验值
        @param exp: int 经验值
        @param status: int 表示是否及时推送升级消息
        """
        if exp ==self._exp:
            return
        if self._level>=self.MAXLEVEL:
            return
        status = 0
        self._exp = exp
        while self._exp >= self.getMaxExp():
            self._exp -= self.getMaxExp()
            self._level += 1
            status = 1
        if status:
            self.updateLevel(self._level)
        petmode = tbpetadmin.getObj(self._owner.baseInfo.getId())
        petmode.update_multi({'exp':self._exp})
#        dbCharacterPet.updatePetInfo(self._owner.baseInfo.getId(), {'exp':self._exp})

    def addExp(self,exp,state = 1,update = 1):
        """加经验
        """
        self.updateExp(exp+self.getExp())

    def getLevel(self):
        """获取角色当前等级
        """
        return self._level

    def setLevel(self,level):
        """设置角色当前等级
        @param level: int 等级
        """
        self._level = level

    def updateLevel(self,level):
        """更新角色当前等级
        @param level: int 等级
        """
        self._level = level
        petmode = tbpetadmin.getObj(self._owner.baseInfo.getId())
        petmode.update_multi({'level':self._level})

    def getAllExp(self):
        """获取所有的可传承经验"""
        allExp = 100
        level = self.getLevel()
        while level>1:
            level -=1
            allExp += dbCharacterPet.PET_EXP.get(level)
        allExp += self.getExp()
        return allExp/2

    def ForecastLevelUp(self,exp):
        """预测可能提升的等级"""
        nowallexp = self._exp + exp
        lastlevel = self._level
        if self._level>=self.MAXLEVEL:
            return self.MAXLEVEL
        while nowallexp >= self.getMaxExp():
            nowallexp -= dbCharacterPet.PET_EXP.get(lastlevel)
            lastlevel += 1
        return lastlevel





