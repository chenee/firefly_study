#coding:utf8
"""
Created on 2009-12-2

@author: wudepeng
"""

from app.game.component.Component import Component

class ItemLevelComponent(Component):
    """
    level component for item
    """

    def __init__(self,owner,quality,starLevel):
        """
        Constructor
        """
        Component.__init__(self,owner)
        self._qualityLevel = quality #品质等级
        self._starLevel = starLevel #物品星级

    def getQuality(self):
        """获取物品品质等级"""
        return self._qualityLevel

    def setQuality(self,level):
        """设置物品品质等级"""
        self._qualityLevel = level

    def getStarLevel(self):
        """获取物品星级"""
        return self._starLevel

    def setStarLevel(self,starLevel):
        """设置物品星级"""
        self._starLevel = starLevel




