#coding:utf8
"""
Created on 2011-3-24

@author: sean_lan
"""
from singleton import Singleton

class UsersManager:

    __metaclass__ = Singleton

    def __init__(self):
        self._users = {}

    def addUser(self, user):
        """添加一个用户
        """
        if user.id in self._users:
            self._users[user.id].disconnectClient()
            self.dropUserByID(user.id)
        self._users[user.id] = user

    def getUserByID(self, uid):
        """根据ID获取用户信息
        """
        return self._users.get(uid)

    def getUserByDynamicId(self,dynamicId):
        """根据客户端的动态ID获取user实例"""
        for user in self._users.values():
            if user.dynamicId == dynamicId:
                return user
        return None

    def getUserByUsername(self, username):
        """根据用户名获取用户信息
        """
        for user in self._users.values():
            if user.getNickName() == username:
                return user
        return None

    def dropUser(self, user):
        """处理用户下线
        """
        userId = user.id
        try:
            del self._users[userId]
        except Exception,e:
            print e

    def dropUserByDynamicId(self, dynamicId):
        user = self.getUserByDynamicId(dynamicId)
        if user:
            self.dropUser(user)

    def dropUserByID(self, userId):
        """根据用户ID处理用户下线
        """
        user = self.getUserByID(userId)
        if user:
            self.dropUser(user)
