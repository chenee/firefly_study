#coding:utf8
"""
Created on 2011-3-22

@author: hanbing
"""

from app.game.component.Component import Component

class BaseInfoComponent(Component):
    """
    抽象的基本信息对象
    """

    def __init__(self, owner, bid, basename):
        """
        创建基本信息对象
        @param id: owner的id
        @param name: 基本名称
        """
        Component.__init__(self,owner)
        self.id = bid                   # owner的id
        self._baseName = basename       # 基本名字

    def getId(self):
        return self.id

    def setId(self , bid):
        self.id = bid

    def getName(self):
        return self._baseName

    def setName(self,name):
        self._baseName = name


