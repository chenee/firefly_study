#coding:utf8
"""
Created on 2013-8-2

@author: lan (www.9miao.com)
"""
from singleton import Singleton

class GlobalObject:

    __metaclass__ = Singleton

    def __init__(self):
        self.db = None
        self.stophandler = None
        # self.webroot = None
        self.leafNode = None
        self.reloadmodule = None
        self.root = None
        self.localservice = None


# def masterserviceHandle(target):
#     """
#     """
#     GlobalObject().leafNode._service.mapTarget(target)
#
# def netserviceHandle(target):
#     """
#     """
#     GlobalObject().netfactory.service.mapTarget(target)
#
def addToRootService(target):
    """
    """
    GlobalObject().root.service.mapTarget(target)
#
# class webserviceHandle:
#     """这是一个修饰符对象
#     """
#
#     def __init__(self,url=None):
#         """
#         @param url: str http 访问的路径
#         """
#         self._url = url
#
#     def __call__(self,cls):
#         """
#         """
#         if self._url:
#             GlobalObject().webroot.putChild(self._url, cls())
#         else:
#             GlobalObject().webroot.putChild(cls.__name__, cls())
#
#
#
# class remoteserviceHandle:
#     """
#     """
#     def __init__(self,remotename):
#         """
#         """
#         self.remotename = remotename
#
#     def __call__(self,target):
#         """
#         """
#         GlobalObject().remote[self.remotename]._reference._service.mapTarget(target)

