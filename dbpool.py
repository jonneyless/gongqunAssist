import pymysql
from dbutils.pooled_db import PooledDB

from config import mysqlInfo


class OPMysql(object):
    __pool = None

    def __init__(self):
        self.coon = OPMysql.getmysqlconn()
        self.cur = self.coon.cursor(cursor=pymysql.cursors.DictCursor)

    # 数据库连接池连接
    @staticmethod
    def getmysqlconn():
        if OPMysql.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                              host=mysqlInfo['host'],
                              db=mysqlInfo['db'],
                              user=mysqlInfo['user'],
                              passwd=mysqlInfo['passwd'],
                              port=mysqlInfo['port']
                              )

        return __pool.connection()

    # 插入\更新\删除
    def op_update(self, sql):
        self.cur.execute(sql)
        self.coon.commit()
        lastrowid = self.cur.lastrowid

        return lastrowid

    # 查询
    def op_select_one(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchone()
        return select_res

    # 查询
    def op_select_all(self, sql):
        self.cur.execute(sql)
        select_res = self.cur.fetchall()
        return select_res

    # 释放资源
    def dispose(self):
        self.coon.close()
        self.cur.close()
