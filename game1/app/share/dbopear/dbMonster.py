#coding:utf8
"""
Created on 2011-8-12

@author: SIOP_09
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor

All_MonsterInfo = {}

def getAllMonsterInfo():
    """获取所有怪物的信息
    """
    global All_MonsterInfo
    sql = "SELECT * FROM tb_monster"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for monster in result:
        All_MonsterInfo[monster['id']] = monster




