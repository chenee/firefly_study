#coding:utf8
"""
Created on 2012-2-21
殖民管理器
@author: jt
"""
from singleton import Singleton
from twisted.python import log
from app.share.dbopear import dbLanguage


class Lg:
    """殖民管理器"""
    __metaclass__ = Singleton

    def __init__(self):
        """初始化"""
        self.info={}#key:表id ， value:翻译之后的内容
        self.info=dbLanguage.getAll()
        
    def update(self):
        """更新数据信息"""
        self.info=dbLanguage.getAll()
        
    def g(self,gid):
        """根据id获取翻译信息"""
        try:
            info= self.info.get(gid)
            if not info:
                log.err(str(gid))
                return str(gid)
            return info
        except:
            return str(id)
            log.err("%s不存在"%gid)
       
    
