#coding:utf8
"""
Created on 2011-3-22

@author: sean_lan
"""

from app.game.component.baseInfo.BaseInfoComponent import BaseInfoComponent


class CharacterBaseInfoComponent(BaseInfoComponent):
    """玩家基础信息组件类"""
    def __init__(self, owner, cid, nickName=u"",viptype=1):
        """
        Constructor
        """
        BaseInfoComponent.__init__(self, owner, cid, nickName)
        self._viptype = viptype  #玩家类型


    #----------------nickName-----------

    def setnickName(self,nickName):#从数据库中读取后赋值
        self._baseName = nickName

    def getNickName(self):#获取内存中的值
        return self._baseName

    def setType(self ,viptype):#
        self._viptype = viptype

    def getType(self):
        return self._viptype

