#coding:utf8
"""
Created on 2012-7-1
竞技场信息
@author: Administrator
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor
import util
import datetime

def getCharacterArenaInfo(characterId):
    """获取角色竞技场信息
    @param characterId: int 角色的ID
    """
    sql = "SELECT * FROM tb_arena where characterId =%d"%characterId
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        insertCharacterArenaInfo(characterId)
        result = {'characterId':characterId,'score':0,'liansheng':0,
                  'lastresult':0,'lasttime':datetime.datetime(2012,6,20,12),
                  'ranking':0,'surplustimes':15,'buytimes':0,'receive':0,
                  'recorddate':datetime.date.today()}
    return result

def insertCharacterArenaInfo(characterId):
    """插入角色竞技场信息
    """
    datestr = datetime.date.today()
    sql = "insert into tb_arena(characterId,recorddate,ranking)\
     values(%d,'%s',%d)"%(characterId,datestr,characterId-1000000)
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()

def updateCharacterArenaInfo(characterId,props):
    """更新角色的竞技场信息
    """
    sqlstr = util.forEachUpdateProps('tb_arena', props,{'characterId':characterId})
    conn = dbpool.connection()
    cursor = conn.cursor()
    count = cursor.execute(sqlstr)
    conn.commit()
    cursor.close()
    conn.close()
    if count >= 1:
        return True
    else:
        return False

def getCharacterArenaRank(characterId):
    """获取角色的排名
    """
    sql = "SELECT ranking from tb_arena where characterId = %d;"%(characterId)
    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result[0]
    else:
        return 0


def forEachSelectORByList(fieldname,valueslist):
    """遍历字典，生成查询或（关系的）sql语句"""
    sqlstr = ''
    joinstrlist = []
    for index,value in enumerate( valueslist):
        if index==0:
            joinstrlist.append(" %s = %d"%(fieldname,value))
        else:
            joinstrlist.append(" or %s = %d"%(fieldname,value))
    sqlstr = sqlstr.join(joinstrlist)
    return sqlstr

def getCharacterRivalList(ranklist):
    """获取角色的对手列表
    """
    orsql = forEachSelectORByList('b.ranking', ranklist)
    if orsql:
        sql = "SELECT b.characterId,b.ranking,\
        a.nickname,a.level,a.profession from tb_character as a,\
        tb_arena as b where a.id=b.characterId and (%s) order by `ranking`;"%(orsql)
    else:
        return []
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def getCharacterBattleLog(characterId):
    """获取角色战斗日志
    """
    sql = "SELECT * from tb_arena_log where tiaozhan = %d \
    or yingzhan = %d order by recordtime desc limit 0,5;"%(characterId,characterId)
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def insertBattleLog(characterId,tocharacterId,fname,tname,success,rankingChange):
    """插入战斗日志
    """
    sql = "insert into tb_arena_log(tiaozhan,yingzhan,\
    tiaozhanname,yingzhanname,success,rankingChange)\
     values(%d,%d,'%s','%s',%d,%d)"%(characterId,\
                                     tocharacterId,fname,tname,success,rankingChange)

    conn = dbpool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    cursor.close()
    conn.close()



