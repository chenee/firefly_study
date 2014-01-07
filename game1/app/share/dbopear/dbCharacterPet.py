#coding:utf8
"""
Created on 2011-12-14

@author: lan (www.9miao.com)
"""

from dbpool import dbpool

PET_TRAIN_CONFIG = {}
PET_TEMPLATE = {}#宠物模板表
PET_TYPE = {}
PET_EXP = {}
PET_GROWTH = {}

#shopAll1=[]#灵兽商店50以下所有宠物
shopAll={1:[],2:[],3:[],4:[]}#    1高级宠物  2中级宠物  3低级宠物 根据宠物颜色来
shopXy=[]#50以幸运领取的宠物

##shopAll2=[]#幻兽商店50-70
#shopAll2={1:[],2:[],3:[]}#幻兽商店50-70   1高级宠物  2中级宠物  3低级宠物
#shopXy2=[]#50-70 幸运领取的宠物
#
##shopAll3=[]#圣兽商店70以上
#shopAll3={1:[],2:[],3:[]}#圣兽商店70以上      1高级宠物  2中级宠物  3低级宠物
#shopXy3=[]#70以上 幸运领取的宠物

def getPetExp():
    """获取宠物的经验表"""
    global PET_EXP
    sql = "SELECT * FROM tb_pet_experience"
    result = dbpool.fetchAll(sql)
    for exp in result:
        PET_EXP[exp['level']] = exp['ExpRequired']
        
def getAllPetGrowthConfig():
    """获取宠物成长配置
    """
    global PET_GROWTH
    sql = "SELECT * FROM tb_pet_growth"
    result = dbpool.fetchAll(sql)

    for growthconfig in result:
        attrType = growthconfig['pettype']
        quality = growthconfig['quality']
        if not PET_GROWTH.has_key(attrType):
            PET_GROWTH[attrType] = {}
        PET_GROWTH[attrType][quality] = growthconfig

def getAllPetTemplate():
    """获取宠物的模板信息"""
    global PET_TEMPLATE,shopAll,shopXy,PET_TYPE
    sql = "SELECT * FROM tb_pet_template ORDER BY `level` , `id`;"
    result = dbpool.fetchAll(sql)

    for pet in result:
        attrType = pet['attrType']
        if not PET_TYPE.has_key(attrType):
            PET_TYPE[attrType] = []
        PET_TYPE[attrType].append(pet['id'])
        PET_TEMPLATE[pet['id']] = pet

        if pet['coin']>0:
            zi=pet['baseQuality']
            shopAll[zi].append(pet['id'])
        if pet['xy']>0:
            shopXy.append(pet)
            

def getPetTrainConfig():
    """获取宠物培养配置信息"""
    global PET_TRAIN_CONFIG
    sql = "SELECT * FROM tb_pet_training "
    result = dbpool.fetchAll(sql)
    for train in result:
        PET_TRAIN_CONFIG[train['quality']] = train
    return result
    
