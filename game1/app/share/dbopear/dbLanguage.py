#coding:utf8
"""
Created on 2011-8-19

@author: SIOP_09
"""
from dbpool import dbpool

def getAll():
    """获取所有翻译信息"""
    sql="SELECT * FROM tb_language"
    result = dbpool.fetchAll(sql)

    if not result:
        return None
    data={}
    for item in result:
        data[item['id']]=item['content']
    return data

