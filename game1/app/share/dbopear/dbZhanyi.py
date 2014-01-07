#coding:utf8
"""
Created on 2013-1-8
战役相关数据库操作
@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor


ALL_ZHANYI_INFO = {}#所有的战役的信息
ALL_ZHANGJIE_INFO = {}#所有章节的信息
ALL_ZHANGJIE_GROP = {}#战役与章节关系

def getAllZhanYiInfo():
    """获取所有战役的信息
    """
    global ALL_ZHANYI_INFO
    sql = "SELECT * FROM tb_zhanyi"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for zhanyi in result:
        ALL_ZHANYI_INFO[zhanyi['id']] = zhanyi


def getAllZhangJieInfo():
    """获取章节的信息
    """
    global ALL_ZHANGJIE_INFO,ALL_ZHANGJIE_GROP
    sql = "SELECT * FROM tb_zhangjie"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for zhangjie in result:
        ALL_ZHANGJIE_INFO[zhangjie['id']] = zhangjie
        if not ALL_ZHANGJIE_GROP.get(zhangjie['yid']):
            ALL_ZHANGJIE_GROP[zhangjie['yid']] = []
        ALL_ZHANGJIE_GROP[zhangjie['yid']].append(zhangjie['id'])





