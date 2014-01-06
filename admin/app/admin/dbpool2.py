#coding:utf8
"""
Created on 2012-4-9

@author: Administrator
"""
from twisted.python import log
from MySQLdb.cursors import DictCursor
from Queue import Queue
import MySQLdb

class PoolException(Exception):
    pass

DBCS = {'mysql':MySQLdb.connect}


class UCursor:
    """自定义游标对象"""

    def __init__(self,conn,cursorclass):
        """
        @param conn: conn 数据库连接对象
        """
        self.conn = conn
        if cursorclass:
            self.cursor = conn.cursor(cursorclass=cursorclass)
        else:
            self.cursor = conn.cursor()

    def execute(self,sql):
        """语句执行
        @param sql: str sql 语句
        """
        count = self.cursor.execute(sql)
        return count

    def executemany(self,sql,args):
        """语句执行
        @param sql: str sql 语句
        """
        count = self.cursor.executemany(sql,args)
        return count

    def fetchall(self):
        """获取所有游标对象中的数据"""
        return self.cursor.fetchall()

    def fetchone(self):
        """获取所有游标对象中的一条数据"""
        return self.cursor.fetchone()

    def close(self):
        """删除游标对象"""
        self.cursor.close()
        self.conn.close()


class DBPool(object):
    """''一个数据库连接池"""

    def initPool(self, maxActive=5, maxWait=None, init_size=1, db_type="mysql", **config):
        """初始化数据库连接池
        """
        log.msg("__init__ Pool..")
        self.__freeConns = Queue(maxActive)
        self.maxWait = maxWait
        self.db_type = db_type
        self.config = config
        if init_size > maxActive:
            init_size = maxActive
        for i in range(init_size):
            self.free(self._create_conn())
        self.nowconn = None

    def __del__(self):
        log.msg("__del__ Pool..")
        self.release()

    def release(self):
        """''释放资源，关闭池中的所有连接"""
        log.msg("release Pool..")
        while self.__freeConns and not self.__freeConns.empty():
            con = self.get()
            con.release()
            self.__freeConns = None

    def _create_conn(self):
        """''创建连接 """
        if self.db_type in DBCS:
            return MySQLdb.connect(**self.config);

    def get(self, timeout=None):
        """''获取一个连接
        @param timeout:超时时间
        """
        if timeout is None:
            timeout = self.maxWait
            conn = None
        if self.__freeConns.empty():#如果容器是空的，直接创建一个连接
            conn = self._create_conn()
        else:
            conn = self.__freeConns.get(timeout=timeout)
            conn.pool = self
        return conn

    def cursor(self,cursorclass = None):
        """通配接口"""
        conn = self.get()
        self.nowconn = conn
        ucur = UCursor( conn, cursorclass)
        return ucur

    def commit(self):
        """提交"""
        try:
            self.nowconn.commit()
        except Exception as e:
            log.err(e.message)
    def rollback(self):
        """事务回滚
        """
        try:
            self.nowconn.rollback()
        except Exception as e:
            log.err(e.message)

    def free(self, conn):
        """''将一个连接放回池中
        @param conn: 连接对象
        """
        conn.pool = None
        if(self.__freeConns.full()):#如果当前连接池已满，直接关闭连接
            conn.release()
        return self.__freeConns.put_nowait(conn)

    def execSql(self,sqlstr):
        """执行数据库的写操作(插入,修改,删除)
        @param sqlstr: str 需要执行的sql语句
        """
        try:
            conn = self.get(5)
            cursor = conn.cursor()
            count = cursor.execute(sqlstr)
            conn.commit()
            cursor.close()
            conn.close()
            if count>0:
                return True
            return False
        except Exception,err:
            log.err(err)
            conn.close()
            return None#通过放回NONE在远程调用上抛出异常

    def execute(self,sqlstrList):
        """批量处理sql语句并且支持事务回滚
        @param sqlstrList: list(str) 需要执行的sql语句list
        """
        try:
            conn = self.get(5)
            cursor = conn.cursor()
            conn.autocommit(False)
            for sqlstr in sqlstrList:
                count = cursor.execute(sqlstr)
                if count<0:
                    raise
            else:
                conn.commit()
                conn.autocommit(True)
                cursor.close()
                conn.close()
                return True
        except Exception,err:
            conn.rollback()   #出现异常，事务回滚
            cursor.close()
            conn.close()
            log.err(err)
            return False

    def querySql(self,sqlstr,dictcursor = False):
        """执行数据库的查询"""
        try:
            conn = self.get(0)
            if dictcursor:
                cursor = conn.cursor(cursorclass=DictCursor)
            else:
                cursor = conn.cursor()
            cursor.execute(sqlstr)
            result = cursor.fetchall()
            cursor.close()
            conn.close()
            return result
        except Exception,err:
            log.err(err)
            conn.close()
            return None#通过放回NONE在远程调用上抛出异常

