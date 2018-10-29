import MySQLdb

# sql = '/*--user=applist;--password=Fs9006;--host=172.16.130.202;--port=3306;--enable-check;*/\
# inception_magic_start;\
# use applist;\
# UPDATE testt SET money=300 WHERE username="gg";\
# inception_magic_commit;'
sql = '/*--user=root;--password=yearning;--host=47.98.255.80;--port=3306;--enable-check;*/\
inception_magic_start;\
BEGIN; \
use Yearning;\
update core_account SET email="test@qq.com" where username="liziyang";\
inception_magic_commit;'


def conn():
    try:
        conn = MySQLdb.connect(host='172.17.69.231', user='', passwd='', db='', port=6669)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        ##
        conn.close()
        num_fields = len(cur.description)
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


def affect(sql):
    conn = MySQLdb.connect(host='172.16.130.202', user='applist', passwd='Fs9006', db='applist', )
    cur = conn.cursor()
    print(sql)
    line = cur.execute(sql)
    result = cur.fetchall()
    print(result, line)
    conn.close()


# conn()
sql = "BEGIN;UPDATE testt SET money=1100 WHERE username='gg';ROLLBACK;"
sql2 = "UPDATE testt SET money=100 WHERE age=22"
sql3 = "select * from testt"
affect(sql2)
