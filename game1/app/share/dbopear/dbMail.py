#coding:utf8
"""
Created on 2011-8-8

@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from twisted.python import log
import util

LEVEL_MAIL = {}#所有等级的邮件提示


def forEachQueryProps(sqlstr, props):
    """遍历所要查询属性，以生成sql语句"""
    if props == '*':
        sqlstr += ' *'
    elif type(props) == type([0]):
        i = 0
        for prop in props:
            if(i == 0):
                sqlstr += ' ' + prop
            else:
                sqlstr += ', ' + prop
            i += 1
    else:
        log.msg('props to query must be list')
        return
    return sqlstr

def getAllLevelMail():
    """获取所有的等级邮件提示
    """
    global  LEVEL_MAIL
    sql = "SELECT * FROM tb_levelmail"
    result = dbpool.fetchAll(sql)

    scenesInfo = {}
    for scene in result:
        scenesInfo[scene['level']] = scene
    LEVEL_MAIL = scenesInfo
    return scenesInfo


def getPlayerMailCnd(characterId,mtype):
    """获取角色邮件列表长度
    @param characterId: int 角色的ID
    @param type: int 邮件的分页类型
    """
    cnd = 0
    if mtype ==0:
        cnd = getPlayerAllMailCnd(characterId)
    elif mtype ==1:
        cnd = getPlayerSysMailCnd(characterId)
    elif mtype ==2:
        cnd = getPlayerFriMailCnd(characterId)
    elif mtype ==3:
        cnd = getPlayerSavMailCnd(characterId)
    return cnd

def getPlayerAllMailCnd(characterId):
    """获取玩家所有邮件的数量"""
    sql = "SELECT COUNT(`id`) FROM tb_mail WHERE receiverId = %d and isSaved = 0"%characterId
    result = dbpool.fetchOne(sql)

    return result[0]

def getPlayerFriMailCnd(characterId):
    """获取角色玩家邮件的数量"""
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `type`=1  and isSaved = 0"%characterId
    result = dbpool.fetchOne(sql)

    return result[0]

def getPlayerSysMailCnd(characterId):
    """获取角色系统邮件数量"""
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `type`=0  and isSaved = 0"%characterId
    result = dbpool.fetchOne(sql)

    return result[0]

def getPlayerSavMailCnd(characterId):
    """获取保存邮件的数量"""
    sql = "SELECT COUNT(id) FROM tb_mail WHERE receiverId = %d AND `isSaved`=1"%characterId
    result = dbpool.fetchOne(sql)

    conn.close()
    return result[0]

def getPlayerMailList(characterId):
    """获取角色邮件列表"""
    data = getPlayerAllMailList(characterId)
    return data


def getPlayerAllMailList(characterId):
    """获取角色邮件列表
    @param characterId: int 角色的id
    """
    filedList = ['id','sender','title','type','isReaded','sendTime']
    sqlstr = ''
    sqlstr = forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d  and isSaved = 0\
     order by isReaded ,sendTime desc"%(sqlstr,characterId)
    result = dbpool.fetchAll(sql)

    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            if filedList[i]=='sendTime':
                mailInfo['sendTime'] = str(mail[i])
            else:
                mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerSysMailList(characterId,page,limit):
    """获取角色邮件列表
    @param characterId: int 角色的id
    """
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `type`=0  and isSaved = 0\
     order by isReaded,sendTime desc LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    result = dbpool.fetchAll(sql)

    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerFriMailList(characterId,page,limit):
    """获取角色邮件列表
    @param characterId: int 角色的id
    """
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `type`=1  and isSaved = 0\
     order by isReaded LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    result = dbpool.fetchAll(sql)

    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def getPlayerSavMailList(characterId,page,limit):
    """获取角色邮件列表
    @param characterId: int 角色的id
    """
    filedList = ['id','title','type','isReaded','sendTime','content']
    sqlstr = ''
    sqlstr = forEachQueryProps(sqlstr, filedList)
    sql = "select %s from `tb_mail` where receiverId = %d and `isSaved`=1\
     order by isReaded LIMIT %d,%d "%(sqlstr,characterId,(page-1)*limit,limit)
    result = dbpool.fetchAll(sql)

    data = []
    for mail in result:
        mailInfo = {}
        for i in range(len(mail)):
            mailInfo[filedList[i]] = mail[i]
        data.append(mailInfo)
    return data

def checkMail(mailId,characterId):
    """检测邮件是否属于characterId
    @param characterId: int 角色的ID
    @param mailId: int 邮件的ID
    """
    sql = "SELECT `id` FROM tb_mail WHERE id = %d AND receiverId=%d"%(mailId,characterId)
    result = dbpool.fetchOne(sql)

    if result:
        return True
    return False

def getMailInfo(mailId):
    """获取邮件详细信息"""
    sql = "select * from `tb_mail` where id = %d"%(mailId)
    result = dbpool.fetchOne(sql, 1)

    return result

def updateMailInfo(mailId,prop):
    """更新邮件信息"""
    sql = util.forEachUpdateProps('tb_mail',prop, {'id':mailId})
    count = dbpool.executeSQL(sql)
    if(count >= 1):
        return True
    return False

def addMail(title,senderId,sender,receiverId,content,mailtype):
    """添加邮件"""
    sql = "INSERT INTO tb_mail(title,senderId,sender,receiverId,\
    `type`,content,sendTime) VALUES ('%s',%d,'%s',%d,%d,'%s',\
    CURRENT_TIMESTAMP())"%(title,senderId,sender,receiverId,mailtype,content)
    count = dbpool.executeSQL(sql)

    if count >= 1:
        return True
    return False

def deleteMail(mailId):
    """删除邮件"""
    sql = "DELETE FROM tb_mail WHERE id = %d"%mailId
    count = dbpool.executeSQL(sql)

    if count >= 1:
        return True
    return False

