#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor


tb_Experience_config = {}
VIPEXP = {}

def getExperience_Config():
    """获取经验配置表信息"""
    global tb_Experience_config
    sql = "select * from tb_experience"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    for _item in result:
        tb_Experience_config[_item['level']] = _item

def getVIPExp():
    global VIPEXP
    sql = "SELECT * FROM tb_vipexp"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    for vipp in result:
        VIPEXP[vipp['viplevel']] = vipp['maxexp']






