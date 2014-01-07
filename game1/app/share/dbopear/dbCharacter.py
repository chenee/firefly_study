#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from twisted.python import log
import util


def updatePlayerDB(player):
    """更新角色的数据库信息"""
    characterId = player.baseInfo.id
    props = {'level':player.level.getLevel(),'coin':player.finance.getCoin(),
             'exp':player.level.getExp(),'hp':player.attribute.getHp()}
    sqlstr = util.forEachUpdateProps('tb_character',props, {'id':characterId})
    count = dbpool.executeSQL(sqlstr)
    if count >= 1:
        return True
    else:
        log.err(sqlstr)
        return False

def getCharacterIdByNickName(nickname):
    """根据昵称获取角色的id
    @param nickname: string 角色的昵称
    """
    sql = "select id from `tb_character` where nickname ='%s'"%nickname
    dbpool.fetchOne(sql)
    return result

def getALlCharacterBaseInfo():
    """获取所有的角色的基础信息
    """
    sql = "SELECT `id`,`level`,`profession`,`nickname` FROM tb_character;";
    result = dbpool.fetchAll(sql)

    return result




