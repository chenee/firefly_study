#coding:utf8
"""
Created on 2013-8-15

@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor
from app.game.core.Item import Item
from twisted.python import log
import random

DROPOUT_CONFIG = {}
BASERATE=100000 #几率的基数

def getAll():
    """获取所有掉落信息"""
    global DROPOUT_CONFIG
    sql="select * from tb_dropout"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return None
    for item in result:
        item['itemid']=eval("["+item['itemid']+"]")
        DROPOUT_CONFIG[item['id']]=item


def getDropByid(did):
    """根据怪物id获取掉落物品信息 (适用于 怪物掉落 返回一个掉落物品)
    @param did: int 怪物掉落表主键id
    """
    data=DROPOUT_CONFIG.get(did,None)
    if not data:
        log.err(u'掉落表填写错误不存在掉落信息-掉落主键:%d'%did)
        return None
    for item in data.get('itemid'):
        abss=random.randint(1,BASERATE)
        if abss>=1 and abss<=item[2]:#如果随机出来此物品
            abss=random.randint(1,item[1]) #物品数量
            item1=Item(item[0])
            item1.pack.setStack(abss)
            return item1
    return None

