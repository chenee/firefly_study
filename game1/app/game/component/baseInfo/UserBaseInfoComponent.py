#coding:utf8
"""
Created on 2011-3-23

@author: sean_lan
"""
from component.baseInfo.BaseInfoComponent import BaseInfoComponent

class UserBaseInfoComponent(BaseInfoComponent):
    """用户基础信息组件类"""
    def __init__(self ,owner,id ,name ='',character_1 =0,character_2=0,\
                 character_3 = 0,character_4=0,character_5 = 0, pid = 0):
        """
        @character_1 (int) 用户的第一个角色id
        @character_2 (int) 用户的第二个角色id
        @character_3 (int) 用户的第三个角色id
        @character_4 (int) 用户的第四个角色id
        @pid (int) 用户邀请角色的 id
        """
        BaseInfoComponent.__init__(self,owner, id, name)
        self.character_1 = character_1
        self.character_2 = character_2
        self.character_3 = character_3
        self.character_4 = character_4
        self.character_5 = character_5
        self.pid = pid

    #--------------character_1----------------
    def setCharacter_1(self, id):
        self.character_1=id

    def getCharacter_1(self):
        return self.character_1

    def updateCharacter_1(self, id):
        self.character_1=id

    #--------------character_2----------------
    def setCharacter_2(self, id):
        self.character_2=id

    def getCharacter_2(self):
        return self.character_2

    def updateCharacter_2(self, id):
        self.character_2=id

    #--------------character_3----------------
    def setCharacter_3(self, id):
        self.character_3=id

    def getCharacter_3(self):
        return self.character_3

    def updateCharacter_3(self, id):
        self.character_3=id

    #--------------character_4----------------
    def setCharacter_4(self, id):
        self.character_4=id

    def getCharacter_4(self):
        return self.character_4

    def updateCharacter_4(self, id):
        self.character_4=id

    #--------------character_5----------------
    def setCharacter_5(self, id):
        self.character_5=id

    def getCharacter_5(self):
        return self.character_5

    def updateCharacter_5(self, id):
        self.character_5=id

    #--------------pid--------------------
    def setPid(self, id):
        self.pid=id

    def getPid(self):
        return self.pid

