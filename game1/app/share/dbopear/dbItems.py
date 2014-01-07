#coding:utf8
"""
Created on 2011-7-14
对物品表（tb_item）的操作
@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor

all_ItemTemplate = {} #所有的物品模板信息
ALL_SETINFO = {}


def getAll_ItemTemplate():
    """获取所有的物品信息
    """
    global all_ItemTemplate
    sql="select * from `tb_item_template`"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    for _item in result:
        all_ItemTemplate[_item['id']] = _item

def getAllsetInfo():
    """获取所有的套装信息
    """
    global ALL_SETINFO
    sql = "SELECT * from tb_equipmentset;"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for setinfo in result:
        ALL_SETINFO[setinfo['id']] = setinfo

