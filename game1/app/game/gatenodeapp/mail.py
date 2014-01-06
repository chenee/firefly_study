#coding:utf8
"""
Created on 2013-7-17

@author: lan (www.9miao.com)
"""
from app.game.gatenodeservice import remoteserviceHandle
import json
from app.game.appinterface import mail

@remoteserviceHandle
def getMailList_501(dynamicId, request_proto):
    """获取邮件列表"""
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    data = mail.getMailList(dynamicId, characterId)
    return json.dumps(data)

@remoteserviceHandle
def sendMail_502(dynamicId, request_proto):
    """发送邮件"""
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    playerName = argument.get('pname')
    title = argument.get('title')
    content = argument.get('content')
    data = mail.sendMail(dynamicId, characterId, playerName, title, content)
    return json.dumps(data)

@remoteserviceHandle
def getMailInfo_505(dynamicId, request_proto):
    """获取邮件内容"""
    argument = json.loads(request_proto)
    characterId = argument.get('characterId')
    mailID = argument.get('mailID')
    data = mail.getMailInfo(dynamicId, characterId, mailID)
    return json.dumps(data)


