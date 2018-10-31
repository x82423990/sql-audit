import MySQLdb


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
        print("cur.description",cur.description)
        print(result)
        field_names = [i[0] for i in cur.description]
        print(field_names)
        for row in result:
            print(row[0], "|", row[1], "|", row[2], "|", row[3], "|", row[4], "|",
                  row[5], "|", row[6], "|", row[7], "|", row[8], "|", row[9], "|", row[10])
        cur.close()
        conn.close()
    except MySQLdb.Error as e:
        # print("Mysql Error %d: %s" % (e.args[0], e.args[1]))
        print(e)


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
    # print(newsql)
    cur = conn.cursor()
    cur.execute("desc %s" % sql)
    table_name = cur.fetchone()[2]
    engine_sql = "show table status where name='%s';" % table_name
    cur.execute(engine_sql)
    engine = cur.fetchone()[1]
    print(engine)
    if engine == "InnoDB":
        line = cur.execute(sql)
    else:
        raise Exception("非InnoDB的表不适用！")
    conn.close()
    print(line)


# conn()
# sql = "BEGIN;UPDATE testt SET money=1100 WHERE username='gg';ROLLBACK;"
sql2 = "UPDATE testt SET money=80000 WHERE age=22"
sql3 = "UPDATE test SET count=100 WHERE username='moca'"
sql = '/*--user=root;--password=yearning;--host=47.98.255.80;--port=3306;--enable-check;*/\
inception_magic_start;\
use Yearning;\
update core_account SET email="test@qq.com" where username="liziyang";\
inception_magic_commit;'

sqll = '/*--user=root;--password=Fs9006;--host=172.17.69.231;--port=3306;--enable-execute;*/\
inception_magic_start;\
use test;\
UPDATE test SET count=500 WHERE address="jrc";\
inception_magic_commit;'
conn(sqll)
