#coding:utf8
"""
Created on 2013-8-14

@author: lan (www.9miao.com)
"""
from dbpool import dbpool

ALL_SKILL_INFO = {}
SKILL_GROUP = {}
ALL_BUFF_INFO = {}
PROFESSION_SKILLGROUP = {}

#buff和buff直接的效果配置
BUFF_BUFF = {}
#buff对技能加成配置表
BUFF_SKILL = {}

def getBuffOffsetInfo():
    """获取所有buff之间效果的信息配置
    """
    global BUFF_BUFF
    sql = "SELECT * FROM tb_buff_buff"
    result = dbpool.fetchAll(sql)
    for offset in result:
        if not BUFF_BUFF.has_key(offset['buffId']):
            BUFF_BUFF[offset['buffId']] = {}
        BUFF_BUFF[offset['buffId']][offset['tbuffId']] = offset

def getBuffAddition():
    """获取buff对技能的加成
    """
    global BUFF_SKILL
    sql = "SELECT * FROM tb_buff_skill"
    result = dbpool.fetchAll(sql)

    for addition in result:
        if not BUFF_SKILL.has_key(addition['buffId']):
            BUFF_SKILL[addition['buffId']] = {}
        BUFF_SKILL[addition['buffId']][addition['skillId']] = addition['addition']

def getSkillEffectByID(skillEffectID):
    """获取技能效果ID"""
    sql = "SELECT * FROM tb_skill_effect where effectId=%d"%skillEffectID
    result = dbpool.fetchOne(sql, 1)

    return result

def getAllSkill():
    """初始化技能信息
    #职业技能组
    #技能池
    #技能组
    """
    global  ALL_SKILL_INFO,SKILL_GROUP,PROFESSION_SKILLGROUP
    sql = "SELECT * FROM tb_skill_info"
    result = dbpool.fetchAll(sql)

    for skill in result:
        effectInfo = getSkillEffectByID(skill['effect'])
        skill['effect'] = effectInfo
        ALL_SKILL_INFO[skill['skillId']] = skill
        if not SKILL_GROUP.has_key(skill['skillGroup']):
            SKILL_GROUP[skill['skillGroup']] = {}
        SKILL_GROUP[skill['skillGroup']][skill['level']] = skill
    #初始化职业技能组ID
    for groupID in SKILL_GROUP:
        skillInfo = SKILL_GROUP[groupID].get(1)
        profession = skillInfo.get('profession',0)
        if not PROFESSION_SKILLGROUP.has_key(profession):
            PROFESSION_SKILLGROUP[profession] = []
        PROFESSION_SKILLGROUP[profession].append(groupID)

def getBuffEffect(buffEffectID):
    """获取buff效果"""
    sql = "SELECT * FROM tb_buff_effect where buffEffectID = %d"%buffEffectID
    result = dbpool.fetchOne(sql, 1)

    return result

def getAllBuffInfo():
    """获取所有技能的信息"""
    global ALL_BUFF_INFO
    sql = "SELECT * FROM tb_buff_info"
    result = dbpool.fetchAll(sql)

    for buff in result:
        ALL_BUFF_INFO[buff['buffId']] = buff
        effectInfo = getBuffEffect(buff['buffEffectID'])
        ALL_BUFF_INFO[buff['buffId']]['buffEffects'] = effectInfo

