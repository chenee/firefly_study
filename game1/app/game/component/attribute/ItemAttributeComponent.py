#coding:utf8
"""
Created on 2011-3-29

@author: sean_lan
"""
from app.game.component.Component import Component
from app.game.memmode import tbitemadmin

class ItemAttributeComponent(Component):
    """物品附加属性"""

    def __init__(self,owner,durability=-1,isBound=0,identification=1,strengthen=0,workout=0):
        """初始化物品附加属性
        @param selfExtraAttributeId: []int list 物品自身附加属性
        @param dropExtraAttributeId: []int list 物品掉落时的附加属性
        @param durability: int 物品的耐久度
        @param identification: int 物品的辨识状态   0:未辨识  1:辨识
        """
        Component.__init__(self,owner)
        self.durability = durability #当前耐久
        self.isBound = isBound

    def getDurability(self):
        """获取物品的耐久度"""
        return self.durability

    def setDurability(self,durability):
        """设置物品的耐久度
        @param durability: int 物品的耐久度
        """
        self.durability = durability

    def updateDurability(self,durability):
        """更新物品的耐久度
        @param durability: int 物品的耐久度
        """
        self.setDurability(durability)
        itemmode = tbitemadmin.getObj(self._owner.baseInfo.getId())
        props = {'durability':durability}
        itemmode.update_multi(props)

    def updateStrengthen(self,count):
        """更新物品的强化
        @param count: int 强化等级
        """
        if self.strengthen!=count:
            self.strengthen = count
            itemmode = tbitemadmin.getObj(self._owner.baseInfo.getId())
            props = {'strengthen':count}
            itemmode.update_multi(props)
            self._owner.updateFJ()

