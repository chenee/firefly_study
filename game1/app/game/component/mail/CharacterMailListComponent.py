#coding:utf8
"""
Created on 2011-4-1

@author: sean_lan
"""
from app.share.dbopear import dbMail

from app.game.component.Component import Component
from app.game.component.mail.Mail import Mail
import math

class CharacterMailListComponent(Component):
    """角色邮件列表组件"""

    def __init__(self,owner,mailList = []):
        """
        @param mailList: [] 邮件列表
        """
        Component.__init__(self, owner)
        self._mailList = mailList

    def getMailCnd(self,mtype):
        """获取邮件数量
        @param mtype: int 邮件的类型  0 全部 1系统 2玩家 3保存
        """
        cnd = dbMail.getPlayerMailCnd(self._owner.baseInfo.id, mtype)
        return cnd

    def checkMyMail(self,mailID):
        """检测是否是自己的邮件"""
        result = dbMail.checkMail(mailID, self._owner.baseInfo.id)
        return result

    def getPageCnd(self,responseMailType,limit=4):
        cnd = self.getMailCnd(responseMailType)
        pageCnd = math.ceil(float(cnd)/limit)
        if pageCnd == 0 :
            pageCnd = 1
        return int(pageCnd)

    def getMailList(self):
        """获取角色邮件列表
        """
        data = {}
        mailList = dbMail.getPlayerMailList(self._owner.baseInfo.id)
        data['maillist'] = mailList
        return data

    def readMail(self,mailID):
        """阅读邮件（将邮件未读状态改为以读状态）
        @param mailID: int 邮件的ID
        """
        result = self.checkMyMail(mailID)
        if not result:
            return {'result':False,'message':u""}
        m = Mail(id = mailID)
        m.updateMainInfo({'isReaded':1})
        data = m.formatMailInfo()
        return {'result':True,'data':data}

    def deleteMail(self,mailID):
        """删除邮件"""
        result = self.checkMyMail(mailID)
        if not result:
            return {'result':False,'message':u""}
        m = Mail(id = mailID)
        result = m.destroyMail()
        return {'result':result,'message':u""}

    def saveMail(self,mailID):
        """保存邮件"""
        result = self.checkMyMail(mailID)
        if not result:
            return {'result':False,'message':u""}
        m = Mail(id = mailID)
        result = m.updateMainInfo({'isSaved':1})
        if not result:
            return {'result':False,'message':u""}
        return {'result':True,'message':u""}

    def BatchDelete(self,mailIDList):
        """批量删除"""
        for mailId in mailIDList:
            result = self.checkMyMail(mailId)
            if not result:
                return {'result':False,'message':u""}
        for mailId in mailIDList:
            m = Mail(id = mailId)
            result = m.destroyMail()
        return {'result':True,'message':u""}

    def sendMail(self,receiverId,title,content):
        """发送邮件
        @param receiverId: int 发送者的ID
        @param title: str 邮件的标题
        @param content: str 邮件的内容
        """
        m = Mail( title=title, senderId =self._owner.baseInfo.id, receiverId=receiverId,\
                            sender = self._owner.baseInfo.getNickName(),content=content)
        result = m.mailIntoDB()
        return result

