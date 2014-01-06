#-*-coding:utf8-*-
"""
Created on 2013-4-27

@author: lan
"""
from singleton import Singleton
from app.share.dbopear import dbCharacter
from memclient import mclient
from mcharacter import Mcharacter

class McharacterManager:

    __metaclass__ = Singleton

    def __init__(self):
        """初始化
        @param fortresss: dict{fortressID:fortress} 所有要塞的集合
        """

    def initData(self):
        """初始化角色信息
        """    
        allmcharacter = dbCharacter.getALlCharacterBaseInfo()
        for cinfo in allmcharacter:
            pid = cinfo['id']
            mcha = Mcharacter(pid, 'character%d' % pid, mclient)
            mcha.initData(cinfo)
            mcha.insert()

    def GetCharacterInfoById(self,pid):
        """
        """
        mcha = Mcharacter(pid, 'character%d' % pid,mclient)
        return mcha.mcharacterinfo

    def getMCharacterById(self, pid):
        """
        """
        mcha = Mcharacter(pid, 'character%d' % pid,mclient)
        return mcha




