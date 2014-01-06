#-*-coding:utf8-*-
"""
Created on 2013-4-27

@author: lan
"""
from memobject import MemObject

class Mcharacter(MemObject):

    def __init__(self,pid,name,mc):
        """初始化城镇要塞对象
        @param territoryId: int 领地的ID
        @param guard: int 殖民者的ID
        @param guardname: str 殖民者的名称
        @param updateTime: int 领地被更新的时间
        """
        MemObject.__init__(self, name, mc)
        self.id = pid
        self.level = 0
        self.profession = 0
        self.nickname = u''
        self.guanqia = 1000

    def initData(self,data):
        """初始化殖民地数据
        """
        for keyname in self.__dict__.keys():
            if not keyname.startswith('_'):
                setattr(self,keyname,data.get(keyname))

    @property
    def mcharacterinfo(self):
        keys = [key for key in self.__dict__.keys() if not key.startswith('_')]
        info = self.get_multi(keys)
        return info

