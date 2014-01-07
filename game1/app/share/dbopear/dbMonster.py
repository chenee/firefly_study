#coding:utf8
"""
Created on 2011-8-12

@author: SIOP_09
"""
from dbpool import dbpool

All_MonsterInfo = {}

def getAllMonsterInfo():
    """获取所有怪物的信息
    """
    global All_MonsterInfo
    sql = "SELECT * FROM tb_monster"
    result = dbpool.fetchAll(sql)
    for monster in result:
        All_MonsterInfo[monster['id']] = monster




