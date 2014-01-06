#coding:utf8
"""
Created on 2011-3-31

@author: sean_lan
"""
from app.game.component.Component import Component
from app.share.dbopear import dbExperience


class CharacterLevelComponent(Component):
    """玩家等级组件类
    """
    MAXLEVEL = 100  #满级限制
    MAXVIP = 10  #最大VIP等级
    def __init__(self,owner,level = 1,exp = 0):
        """
        @param owner:  Character Object 组件拥有者
        @param level: int 角色的等级
        @param exp:  int 角色的当前经验
        """
        Component.__init__(self, owner)
        self._level = level
        self._exp = exp
        self._vipexp = 0

    def getVipMaxExp(self):
        """获取当前vip升级所需的最大经验
        """
        return dbExperience.VIPEXP.get(self._owner.baseInfo._viptype)

    def setVipExp(self,exp):
        """初始化VIP经验
        """
        self._vipexp = exp

    def getVipExp(self):
        """获取VIP经验
        """
        return self._vipexp

    def addVipExp(self,exp):
        """加经验"""
        self.updateVIPExp(exp+self.getVipExp())

    def updateVIPExp(self,exp):
        """添加VIP经验
        """
        if exp ==self._vipexp:
            return
        status = 0
        if self._owner.baseInfo._viptype>=self.MAXVIP:#判断是否超过最大VIP等级
            return
        self._vipexp = exp
        while self._vipexp >= self.getVipMaxExp():
            self._vipexp -= self.getVipMaxExp()
            self._owner.baseInfo._viptype += 1
            status = 1
            if self._owner.baseInfo._viptype>=self.MAXVIP:
                break
        if status:
            self._owner.baseInfo.updateType(self._owner.baseInfo._viptype)
        self._owner.pushInfoChanged()

    def getMaxExp(self):
        """计算当前级别的最大经验值"""
        expinfo = dbExperience.tb_Experience_config.get(self._level,{})
        maxExp = expinfo.get('ExpRequired',0)#400 + 60 * (self._level - 1) + 10 * self._level * (self._level + 1) * (self._level - 1)
        return maxExp

    def getExp(self):
        """获取角色当前经验
        """
        return self._exp

    def setExp(self,exp):
        """设置角色当前经验值
        @param exp: int 经验值
        """
        self._exp = exp

    def updateExp(self,exp,state=1,update = 1):
        """更新角色经验值
        @param exp: int 经验值
        @param status: int 表示是否及时推送升级消息
        """
        if exp ==self._exp:
            return
        status = 0
        if self._level>=self.MAXLEVEL:
            return
        self._exp = exp
        while self._exp >= self.getMaxExp():
            self._exp -= self.getMaxExp()
            self._level += 1
            status = 1
        if state:
            if status:
                self.updateLevel(self._level)
                self._owner.attribute.updateHp(self._owner.attribute.getMaxHp())
        else:
            if status:
                self.updateLevel(self._level)
                self._owner.attribute.updateHp(self._owner.attribute.getMaxHp())
                self._owner.msgbox.putPecifiedMsg(1)

    def addExp(self,exp,state = 1,update = 1):
        """加经验"""
        self.updateExp(exp+self.getExp(),state = state,update = update)
#        self._owner.matrix.addPetExp(exp)

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




