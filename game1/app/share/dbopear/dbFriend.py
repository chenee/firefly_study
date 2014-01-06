#coding:utf8
"""
Created on 2011-8-19
@author: SIOP_09
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor
from app.game.core.language.Language import Lg


def addFriend(characterId,playerId,friendType,isSheildedMail=0):
    """添加一个好友
    @param characterId: int 角色的id
    @param playerId: int 好友的id
    @param friendType: int(1,2) 好友的类型 1:好友  2:仇敌
    @param isSheildedMail:int 是否屏蔽邮件 0.不屏蔽邮件 1.屏蔽
    """
    sql = "insert into `tb_friend`(characterId,playerId,friendType,isSheildedMail)\
     values(%d,%d,%d,%d)"%(characterId,playerId,friendType,isSheildedMail)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
        return True
    return False


def deletePlayerFriend(characterId,friendId):
    """删除角色好友
    @param friendId: int 好友编号
    """
    sql = 'delete from `tb_friend` where characterId=%d friendId = %d'%(characterId,friendId)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
        return True
    return False


def getFirendListByFlg(pid,flg):
    """获取角色的所有好友或者黑名单
    @param pid: int 角色id
    @param flg: int 1好友   2黑名单
    """
    sql="SELECT playerId FROM tb_friend WHERE characterId=%s AND friendType=%s"%(pid,flg)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return []
    listdata=[]
    for item in result:
        listdata.append(item['playerId'])
    return listdata

def getFriendTopLevel(characterId,index,limit=20):
    """获取好友的等级排行
    """
    sql = "SELECT id,nickname,level,coin \
    FROM tb_character WHERE `id`!=%d ORDER BY level LIMIT %d,%d;"%(characterId,index,limit)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getFriendTopGuanqia(characterId,index,limit=20):
    """获取好友的关卡排行
    """
    sql = "SELECT id,nickname,`level`,coin FROM tb_character WHERE\
     `id`!=%d ORDER BY guanqia LIMIT %d,%d;"%(characterId,index,limit)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getAllCharacterTop(index,limit=20):
    """获取全服的排行信息
    """
    sql = "SELECT id,nickname,`level`,coin FROM\
     tb_character ORDER BY guanqia LIMIT %d,%d;"%(index,limit)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def UpdateGuYongState(characterId,tid,state):
    """更新好友的雇用状态
    """
    sql = "UPDATE `tb_friend` SET guyong = %d WHERE characterId=%d \
    AND playerId =%d"%(state,characterId,tid)
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
        return True
    return False

def addGuyongRecord(characterId,rolename,zyname,zyid,bresult,coinbound,huoli):
    """添加雇用记录
    """
    sql = "INSERT INTO tb_guyong_record (characterId,\
    chaname,zyname,zyid,battleresult,coinbound,huoli) VALUES \
    (%d,'%s','%s',%d,%d,%d,%d)"%((characterId,rolename,zyname,\
                                  zyid,bresult,coinbound,huoli))
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()
    if count>=1:
        return True
    return False

def getGuyongRecord(characterId):
    sql = "SELECT * FROM tb_guyong_record WHERE \
    characterId = %d ORDER BY reocrddate DESC LIMIT 0,10;"%(characterId)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result= cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getGuYongList(pid):
    """获取角色的所有好友或者黑名单
    @param pid: int 角色id
    """
    sql="SELECT playerId FROM tb_friend WHERE characterId=%s AND guyong=1"%(pid)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return []
    listdata=[]
    for item in result:
        listdata.append(item['playerId'])
    return listdata




