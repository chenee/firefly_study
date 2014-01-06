#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dbpool import dbpool
from MySQLdb.cursors import DictCursor


tb_Profession_Config = {}


def getProfession_Config():
    """获取职业配置表信息"""
    global tb_Profession_Config
    sql = "select * from tb_profession"
    result = dbpool.getSqlResult(sql)

    for _item in result:
        tb_Profession_Config[_item['preId']] = _item


