#coding:utf8
"""
Created on 2009-12-1


"""

class Component(object):
    """
    抽象的组件对象
    """


    def __init__(self, owner):
        """
        创建一个组件
        @param owne: owner of this component
        """
        self._owner = owner

