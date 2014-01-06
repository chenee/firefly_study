#-*-coding:utf8-*-
"""
Created on 2013-6-5

@author: lan (www.9miao.com)
"""
from mmode import MAdmin

tbitemadmin = MAdmin('tb_item', 'id', fk='characterId', incrkey='id')
tbitemadmin.insert()

tb_character_admin = MAdmin('tb_character', 'id', incrkey='id')
tb_character_admin.insert()

tb_zhanyi_record_admin = MAdmin('tb_zhanyi_record', 'id', fk='characterId', incrkey='id')
tb_zhanyi_record_admin.insert()

tb_matrix_amin = MAdmin('tb_character_matrix', 'characterId', incrkey='id')
tb_matrix_amin.insert()

tb_equipment = MAdmin('tb_equipment', 'characterId', incrkey='id')
tb_equipment.insert()

tbpetadmin = MAdmin('tb_pet', 'id', fk='ownerID', incrkey='id')
tbpetadmin.insert()
