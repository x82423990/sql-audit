import MySQLdb
import subprocess
import pymysql


# sql = '/*--user=applist;--password=Fs9006;--host=172.16.130.202;--port=3306;--enable-check;*/\
# inception_magic_start;\
# use applist;\
# UPDATE testt SET money=300 WHERE username="gg";\
# inception_magic_commit;'


def conn(sql):
    try:
        conn = MySQLdb.connect(host='172.17.69.231', user='', passwd='', db='', port=6669)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        ##
        conn.close()
        num_fields = len(cur.description)
        ("cur.description", cur.description)
        (result)
        field_names = [i[0] for i in cur.description]
        (field_names)
        for row in result:
            (row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|",
                  row[5], "|", row[6], "|", row[7], "|", row[8], "|", row[9], "|", row[10])
        cur.close()
        conn.close()
    except MySQLdb.Error as e:
        # ("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        (e)


sqa = '/*--user=root;--password=yearning;--host=47.98.255.80;--port=3306;--enable-check;*/\
inception_magic_start;\
use Yearning;\
update core_account SET email="test@qq.com" where username="liziyang";\
inception_magic_commit;'


# DESC  UPDATE test SET count=100 WHERE name='moca'
def affect(sql):
    db = 'test'
    conn = MySQLdb.connect(user='root', host='172.17.69.231', passwd='Fs9006', db=db, )
    # table_name = sql.split(" ")[1]
    # # 判断数据库执行引擎
    # engine = "show table status where name='%s';" % table_name
    # (newsql)
    cur = conn.cursor()
    cur.execute("desc %s" % sql)
    table_name = cur.fetchone()[2]
    engine_sql = "show table status where name='%s';" % table_name
    cur.execute(engine_sql)
    engine = cur.fetchone()[1]
    (engine)
    if engine == "InnoDB":
        line = cur.execute(sql)
    else:
        raise Exception("非InnoDB的表不适用！")
    conn.close()
    (line)


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
        cur.execute(sql)
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


# # conn()
# # sql = "BEGIN;UPDATE testt SET money=1100 WHERE username='gg';ROLLBACK;"
# sql2 = "UPDATE testt SET money=80000 WHERE age=22"
# sql3 = "UPDATE test SET count=100 WHERE username='moca'"
# sql = '/*--user=root;--password=yearning;--host=47.98.255.80;--port=3306;--enable-check;*/\
# inception_magic_start;\
# use Yearning;\
# update core_account SET email="test@qq.com" where username="liziyang";\
# inception_magic_commit;'
#
# sqll = '/*--user=root;--password=Fs9006;--host=172.17.69.231;--port=3306;--enable-execute;*/\
# inception_magic_start;\
# use test;\
# UPDATE test SET count=500 WHERE address="jrc";\
# inception_magic_commit;'
# conn(sqll)

if __name__ == '__main__':
    import random

    import string

    tmp = "wucai"
    conn = MySQLdb.connect(user="root", host="120.79.128.26", password="Fs9006", db="test", port=3306)
    cur = conn.cursor()
    # sqls = 'INSERT INTO info(username,sex,money) VALUES("%s",1,3306)' % tmp
    # cur = conn.cursor()
    # ret = cur.execute(sqls)
    # conn.commit()
    # cur.close()
    for i in range(1000):
        name = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        a = [1, 2]
        b = random.sample(a, 1)[0]
        money = random.randint(100, 100000)
        (name, b, money)
        sqls = 'INSERT INTO info(username,sex,money) VALUES("%s",%d,%d)' % (name, b, money)
        # cur = conn.cursor()
        ret = cur.execute(sqls)
    conn.commit()
    conn.close()
