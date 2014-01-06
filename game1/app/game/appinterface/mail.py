#coding:utf8
"""
Created on 2011-5-13

@author: sean_lan
"""
from app.game.core.PlayersManager import PlayersManager
from app.share.dbopear import dbShieldWord,dbCharacter

def getMailList(dynamicId,characterId):
    """获取邮件列表
    @param characterId: int 角色的ID
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    mailListInfo = player.mail.getMailList()
    return {'result':True,'data':mailListInfo}

def getMailInfo(dynamicId,characterId,mailID):
    """获取邮件的详细信息
    @param characterId: int 角色的ID
    @param mailID: int 邮件的ID
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    mailInfo = player.mail.readMail(mailID)
    return mailInfo

def SaveAndDeleteMail(dynamicId,characterId,setType,requestInfo,mailId,responseMailType):
    """删除或保存邮件
    @param characterId: int 角色的ID
    @param setType: int 操作类型 0保存1删除单条数据2删除一页数据
    @param requestInfo: int 单条时的邮件ID
    @param mailId: （int）list 批量时邮件的ID列表 
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    if setType ==0:
        result = player.mail.saveMail(requestInfo)
    elif setType==1:
        result = player.mail.deleteMail(requestInfo)
    else:
        result = player.mail.BatchDelete(mailId)
    if result['result']:
        pgcnd = player.mail.getPageCnd(responseMailType)
        result['data']={}
        result['data']['maxPage'] = pgcnd
        result['data']['setTypeResponse'] = setType
    return result

def sendMail(dynamicId,characterId,playerName,title,content):
    """添加邮件
    @param dynamicId: int 客户端的动态id
    @param characterId: int 角色的id
    @param playerName: str 发送人的名称
    @param content: str 邮件内容
    @param title: str 标题
    """
    player = PlayersManager().getPlayerByID(characterId)
    if not player or not player.CheckClient(dynamicId):
        return {'result':False,'message':u""}
    if not dbShieldWord.checkIllegalChar(title):
        return {'result':False,'message':u""}
    if not dbShieldWord.checkIllegalChar(content):
        return {'result':False,'message':u""}
    if len(title)>12:
        return {'result':False,'message':u""}
    toId = dbCharacter.getCharacterIdByNickName(playerName)
    if not toId:
        return {'result':False,'message':u""}
    if toId[0]==characterId:
        return {'result':False,'message':u""}
    result = player.mail.sendMail(toId[0],title,content)
    if  result:
        return {'result':True,'message':u""}
    return {'result':False,'message':u""}


