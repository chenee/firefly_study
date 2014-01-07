#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dbpool import dbpool


tb_Experience_config = {}
VIPEXP = {}

def getExperience_Config():
    """获取经验配置表信息"""
    global tb_Experience_config
    sql = "select * from tb_experience"
    result = dbpool.fetchAll(sql)
    for _item in result:
        tb_Experience_config[_item['level']] = _item

def getVIPExp():
    global VIPEXP
    sql = "SELECT * FROM tb_vipexp"
    result = dbpool.fetchAll(sql)
    for vipp in result:
        VIPEXP[vipp['viplevel']] = vipp['maxexp']






