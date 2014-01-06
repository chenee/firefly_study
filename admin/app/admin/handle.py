#coding:utf8
"""
Created on 2013-9-4

@author: hg (www.9miao.com)
"""

from twisted.web import resource
from twisted.web.resource import ErrorPage
from memmode import register_admin
from globalobject import GlobalObject
from urls import getDayRecordList,getStatistics
import json

class OperaPlayer(resource.Resource):

    def render(self,request):
        username = request.args['username'][0]
        oprea_str = request.args['opera_str'][0]
        usermodedata = register_admin.getObjData(username)#register_admin，注册表的mmode管理器，getObjData(username)，通过主键获取的对应的数据，dict型
        if not usermodedata:
            return "Account does not exist!!!"
        pid = usermodedata.get('characterId')#角色id
        if not pid:
            return "Role does not exist!!!"#角色不存在，创建了账号没有创建人物
        gate_node = GlobalObject().remote.get('gate')
        gate_node.callRemote("opera_player",pid,oprea_str)
        return "Success"


class DayRecored(resource.Resource):
    """获取每日的记录
    """
    def render(self, request):
        index = int(request.args['index'][0])#日前+dd
        data = getDayRecordList(index)
        response = json.dumps(data)
        return response


class Statistics(resource.Resource):
    """单服总数据统计
    """
    def render(self, request):
        data = getStatistics()
        response = json.dumps(data)
        return response







