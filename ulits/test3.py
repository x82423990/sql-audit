# !/usr/bin/python 
import pymysql

# sql = '/* --user=root; --password=Fs9006; --host=172.17.69.231; --port=3306; --enable-check; */ \
# inception_magic_start;\
# use test;\
# CREATE TABLE `classinfodd` (`id` int(2) NOT NULL AUTO_INCREMENT COMMENT "学生id",`classname` varchar(255) DEFAULT NULL COMMENT "班级姓名",`count` int(64) DEFAULT NULL COMMENT "班级人数", PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8; inception_magic_commit;\
# inception_magic_commit;'
sql = '/* --user=root; --password=Fs9006; --host=120.79.128.26; --port=3306; --enable-check; */          inception_magic_start;          use test; CREATE TABLE `classinfodd` (`id` int(2) NOT NULL AUTO_INCREMENT COMMENT "学生id",`classname` varchar(255) DEFAULT NULL COMMENT "班级姓名",`count` int(64) DEFAULT NULL COMMENT "班级人数", PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8; inception_magic_commit;'
try:
    conn = pymysql.connect(host='172.17.69.231', user='', passwd='', db='', port=6669)
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    column_name_max_size = max(len(i[0]) for i in cursor.description)
    row_num = 0
    for result in results:
        row_num = row_num + 1
        print('*'.ljust(27, '*'), row_num, '.row', '*'.ljust(27, '*'))
        row = map(lambda x, y: (x, y), (i[0] for i in cursor.description), result)
        for each_column in row:
            if each_column[0] != 'errormessage':
                print(each_column[0].rjust(column_name_max_size), ":", each_column[1])
            else:
                print(each_column[0].rjust(column_name_max_size), ':',
                      each_column[1].replace('\n', '\n'.ljust(column_name_max_size + 4)))
                cursor.close()
                conn.close()
# except Exception as e:

except pymysql.Error as e:
    print(e)
