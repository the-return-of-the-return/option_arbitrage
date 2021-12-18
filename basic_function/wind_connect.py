#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2019/1/18 9:24
# @Author : xiaochen
# @File   : wind_connect.py


# -*- coding:utf-8 -*-

import pymssql

class MSSQL:
    def __init__(self, host="10.100.103.21", user="connlhtz", pwd="lhtz@2012", db="winddb"):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        if not self.db:
            raise(NameError,"没有设置数据库信息")
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.pwd, database=self.db, charset="utf8")
        cur = self.conn.cursor()
        if not cur:
            raise(NameError,"连接数据库失败")
        else:
            return cur

    def Selsql(self,sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def Allsql(self, creat_sql, insert_sql, sql, drop_sql):
        cur = self.__GetConnect()
        #创建新表
        cur.execute(creat_sql)
        cur.execute(insert_sql)
        print(cur.rowcount)
        cur.execute(sql)
        resList = cur.fetchall()
        cur.execute(drop_sql)

        #查询完毕后必须关闭连接
        self.conn.close()
        return resList

    def Dropsql(self,drop_sql):
        cur = self.__GetConnect()
        cur.execute(drop_sql)
        self.conn.close()

    def Insertsql(self,insert_sql):
        cur = self.__GetConnect()
        cur.execute(insert_sql)

    def Creatsql(self,create_sql):
        cur = self.__GetConnect()
        cur.execute(create_sql)

if __name__ == '__main__':
    ms = MSSQL(host="10.100.106.14", user="connlhtz", pwd="lhtz@2012", db="winddb")
    reslist = ms.Selsql("select top 5 * from TB_OBJECT_0001")
    for i in reslist:
        print(i)

