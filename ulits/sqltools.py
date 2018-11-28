# coding=utf-8
import subprocess
import pymysql

from rest_framework.exceptions import ParseError
from .dbcrypt import prpcrypt
from pymysql.err import ProgrammingError
from _mysql_exceptions import OperationalError, ProgrammingError
import re

class Inception(object):

    def __init__(self, sql=None, dbname=''):
        self.sql = sql
        self.dbname = dbname
        # Inception 数据库地址，用户，密码，端口
        self.inception_ipaddr = '172.16.130.207'
        self.user = 'sqlaudit'
        self.passwd = 'Fs9006'
        self.port = 13306

    def decrypt_password(self, password):
        pc = prpcrypt()
        return pc.decrypt(password)

    def inception_handle(self, dbaddr):
        status = 0
        sql = '/* {} */\
          inception_magic_start;\
          use {}; {} inception_magic_commit;'.format(dbaddr, self.dbname, self.sql)
        try:
            conn = pymysql.connect(host=self.inception_ipaddr, user='', passwd='', port=6669, db='', use_unicode=True,
                                   charset="utf8")  # 连接inception
            cur = conn.cursor()
            try:
                cur.execute(sql)
            except pymysql.err.ProgrammingError as e:
                raise e
            result = cur.fetchall()
            conn.close()
        except pymysql.Error as e:
            status = -1
            result = "Mysql Error {}: {}".format(e.args[0], e.args[1])
        return {'result': result, 'status': status}

    def rows_effect(self, db, host, pwd, port, user, test=None):
        # try:
        password = self.decrypt_password(pwd)
        print("password", password)
        conn = pymysql.connect(user=user, host=host, password=password, db=db, port=port, connect_timeout=5)

        # 测试连通性
        if test is not None:
            return True
        sqls = self.sql.replace("\n", "").split(";")[0:-1]
        lines = 0
        for i in sqls:
            cur = conn.cursor()
            try:
                insert_tag = re.search('insert', i, re.IGNORECASE)
                if insert_tag:
                    table_name = i.split(' ')[2]
                else:
                    cur.execute("desc %s;" % i)
                    table_name = cur.fetchone()[2]
            except (OperationalError, ProgrammingError) as e:
                raise ParseError(e)
            # ("cur.fetchone()", cur.fetchall())

        newsql = "show table status where name='%s';" % table_name
        cur = conn.cursor()
        cur.execute(newsql)
        engine = cur.fetchone()[1]
        if engine == "InnoDB":
            cur = conn.cursor()
            line = cur.execute(i + ";")
            lines += line
        else:
            raise Exception("非InnoDB的表不适用！")
        conn.close()
        return lines


    def manual(self):  # 查询回滚库/表
        conn = pymysql.connect(host=self.inception_ipaddr, port=self.port, user=self.user, passwd=self.passwd,
                               db=self.dbname, charset='utf8')  # 连接SQL备份服务器
        conn.autocommit(True)
        cur = conn.cursor()
        cur.execute(self.sql)
        return cur.fetchall()


    def get_back_table(self):
        return self.manual()[0][0]


    def get_back_sql(self):
        per_rollback = self.manual()
        back_sql = ''  # 回滚语句
        for i in per_rollback:  # 累加
            back_sql += i[0]
        return back_sql


    def get_index_list(self):
        res = self.manual()[3:]
        return [index_info[0] for index_info in res]


class SqlQuery(object):
    def __init__(self, instance):
        self.instance = instance
        self.pc = prpcrypt()

    def decrypt_password(self, password):
        return self.pc.decrypt(password)

    def main(self, sql):  # 查询目标库/表结构
        db = self.instance
        password = self.decrypt_password(db.password)
        try:
            conn = pymysql.connect(host=db.host, port=int(db.port), user=db.user, passwd=password, db=db.name,
                                   charset='utf8')  # 连接目标服务器
        except Exception as e:
            raise ParseError(e)
        conn.autocommit(True)
        cur = conn.cursor()
        try:
            cur.execute(sql)
        except ProgrammingError as e:
            (e)
            return None
        return cur.fetchall()

    def get_tables(self):
        sql = 'show tables;'.format(self.instance.name)
        res = self.main(sql)
        tables = [i[0] for i in res]
        return tables

    def get_table_info(self, table_name):
        sql = 'SHOW CREATE TABLE {}'.format(table_name)
        table_info = self.main(sql)[0][1]
        return table_info

    def sql_advisor(self, sql):
        db = self.instance
        password = self.decrypt_password(db.password)
        cmd_path = '/usr/bin/sqladvisor'
        cmd = "{} -h {} -P {}  -u {} -p '{}' -d {} -q '{};' -v 1".format(cmd_path, db.host, db.port, db.user, password,
                                                                         db.name, sql)
        res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return res.stdout.read()
