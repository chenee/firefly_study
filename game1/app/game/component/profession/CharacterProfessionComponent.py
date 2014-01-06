#coding:utf8
"""
Created on 2011-4-6

@author: sean_lan
"""

from app.game.component.Component import Component
from app.share.dbopear import dbProfession


class CharacterProfessionComponent(Component):
    """
    classdocs
    """
    def __init__(self, owner):
        """
        Constructor
        """
        Component.__init__(self, owner)
        self._profession = 1 #职业
        self._professionStage = 0 #职业阶段
        self._professionPosition = 0 #职位
        self._figure = 0 #角色形象
        self._fashion = 0 #角色的时装
        self._mounts = 0 #角色的坐骑

    def getSceneFigure(self):
        """获取角色的场景形象
        """
        return self._profession

    def getFightFigure(self):
        """获取角色的战斗形象
        """
        return self._profession

    def setFashion(self,fashionId):
        """设置角色的时装
        """
        self._fashion = fashionId

    def setMounts(self,mountsId):
        """设置角色的坐骑
        """
        self._mounts = mountsId

    def getFigure(self):
        """获取角色的形象ID
        """
        return self._profession

    def setFigure(self,figure):
        """设置角色的形象ID
        """
        self._figure = figure

    def getProfession(self):
        return self._profession

    def setProfession(self, profession):
        self._profession = profession

    def getProfessionPosition(self):
        return self._professionPosition

    def setProfessionPosition(self, professionPosition):
        self._professionPosition = professionPosition

    def getProfessionStage(self):
        return self._professionStage

    def setProfessionStage(self, stage):
        self._professionStage = stage

    def getProfessionName(self):
        """得到职业名称"""
        return u"玩家"

    def getProfessionFigure(self):
        """得到玩家形象"""
        return self._profession

    def getOrdinarySkill(self):
        """获取该职业的普通攻击技能"""
        data = dbProfession.tb_Profession_Config[self._profession]
        if data:
            return int(data['ordSkill'])
        return 1001



