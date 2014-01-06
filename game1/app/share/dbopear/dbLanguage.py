#coding:utf8
"""
Created on 2011-8-19

@author: SIOP_09
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor

def getAll():
    """获取所有翻译信息"""
    sql="SELECT * FROM tb_language"
    conn = dbpool.connection()
    cursor = conn.cursor(cursorclass=DictCursor)
    cursor.execute(sql)
    result=cursor.fetchall()
    cursor.close()
    conn.close()
    if not result:
        return None
    data={}
    for item in result:
        data[item['id']]=item['content']
    return data

