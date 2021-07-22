import pandas as pd

import pymysql
import psycopg2
import cx_Oracle
from pyhive import hive
import pymssql


class BaseConnect(object):
    conn = None

    def read_sql(self, sql):
        df = pd.read_sql(sql, self.conn)
        return df

    def close(self):
        self.conn.close()


class MySQL(BaseConnect):
    def __init__(self, db_info):
        self.conn = pymysql.connect(**db_info)


class PostgreSQL(BaseConnect):
    def __init__(self, db_info):
        self.conn = psycopg2.connect(**db_info)


class Oracle(BaseConnect):
    def __init__(self, db_info):
        self.conn = cx_Oracle.connect(**db_info)


class Hive(BaseConnect):
    def __init__(self, db_info):
        self.conn = hive.Connection(**db_info)


class SQLServer(BaseConnect):
    def __init__(self, db_info):
        self.conn = pymssql.connect(**db_info)


dbs = {
    'mysql': MySQL,
    'postgresql': PostgreSQL,
    'oracle': Oracle,
    'hive': Hive,
    'sqlserver': SQLServer,
}

if __name__ == '__main__':
    pass

"""数据库配置文件可为ini格式：

[hive]
host = xx.xx.xx.xx
port = xx
username = xx
password = xx
database = xx
auth = CUSTOM

[postgresql]
host = xx.xx.xx.xx
port = xx
user = xx
password = xx
database = xx

"""
