#coding:utf8
"""
Created on 2013-5-8

@author: lan (www.9miao.com)
"""
from DBUtils.PooledDB import PooledDB
import MySQLdb
from MySQLdb.cursors import DictCursor


DBCS = {'mysql':MySQLdb,}

class DBPool(object):
    """
    """
    def initPool(self,**kw):
        """
        """
        self.config = kw
        self.pool = PooledDB(MySQLdb, 5, host=kw.get("host"), user=kw.get("user"),
                             passwd=kw.get("passwd"), db=kw.get("db"),
                             port=kw.get("port"), charset=kw.get("charset"))

    def connection(self):
        return self.pool.connection()

    def getSqlResult(self, sql):
        conn = dbpool.connection()
        cursor = conn.cursor(cursorclass=DictCursor)
        cursor.execute(sql)
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        return result

dbpool = DBPool()


