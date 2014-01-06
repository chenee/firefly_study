#coding:utf8
"""
Created on 2011-4-21

@author: sean_lan
"""
from app.game.component.Component import Component
from app.game.memmode import tbitemadmin

class ItemPackComponet(Component):
    """物品在包裹中的组件属性
    pack component for item
    """

    def __init__(self,owner,idInPack=0,stack=1):
        """
        Constructor
        """
        Component.__init__(self,owner)
        self._idInPack = idInPack #物品在包裹中的id
        self._stack = stack #可叠加数:'-1:不可叠加1~999:可叠加的数值
#        self._posintion = position #物品在包裹中的位置

    def getPosition(self):
        """获取物品在包裹中的位置"""

    def getIdInPack(self):
        """获取物品在包裹中的id"""
        return self._idInPack

    def setIdInPack(self,idInPack):
        """设置物品在包裹中的id"""
        self._idInPack = idInPack

    def getStack(self):
        return self._stack

    def setStack(self,stack):
        self._stack = stack

    def updateStack(self,stack,tag=0):
        """更新物品层叠数"""
        self._stack = stack
        if stack>0:
            itemmode = tbitemadmin.getObj(self._owner.baseInfo.id)
            props = {'stack':self._stack}
            itemmode.update_multi(props)
        else:
            if tag==0:
                self._owner.destroyItemInDB()


