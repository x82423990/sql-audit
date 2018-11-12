import pymysql
import sqlparse

pymysql.install_as_MySQLdb()


class Inception(object):
    def __init__(self, dbinfo):
        self.__dict__.update(dbinfo)
        self.con = object
        self.host = "172.17.69.231"
        self.port = 6669
        self.user = ""
        self.passwd = ""

    def __enter__(self):
        # un_init = util.init_conf()
        # inception = ast.literal_eval(un_init['inception'])
        try:
            self.con = pymysql.connect(host=self.host,
                                       user=self.user,
                                       passwd=self.passwd,
                                       port=6669,
                                       db='',
                                       charset="utf8")
            (self)
            return self
        except pymysql.Error as e:
            (e)

    def GenerateStatements(self, sql: str = '', types: str = '', backup=None):
        if sql[-1] == ';':
            sql = sql.rstrip(';')
        elif sql[-1] == '；':
            sql = sql.rstrip('；')
        if backup is not None and backup != 0:
            InceptionSQL = '''
             /*--user=%s;--password=%s;--host=%s;--port=%s;%s;%s;*/ \
             inception_magic_start;\
             use `%s`;\
             %s; \
             inception_magic_commit;
            ''' % (self.__dict__.get('user'),
                   self.__dict__.get('password'),
                   self.__dict__.get('host'),
                   self.__dict__.get('port'),
                   types,
                   backup,
                   self.__dict__.get('db'),
                   sql)
            ("------", InceptionSQL)
            return InceptionSQL
        else:
            InceptionSQL = '''
                        /*--user=%s;--password=%s;--host=%s;--port=%s;%s;*/ \
                        inception_magic_start;\
                        use `%s`;\
                        %s; \
                        inception_magic_commit;
                       ''' % (self.__dict__.get('user'),
                              self.__dict__.get('password'),
                              self.__dict__.get('host'),
                              self.__dict__.get('port'),
                              types,
                              self.__dict__.get('db'),
                              sql)
            ("------", InceptionSQL)
            return InceptionSQL

    def Execute(self, sql, backup: int):
        if backup == 1:
            Inceptionsql = self.GenerateStatements(sql=sql, types='--enable-execute')
        else:
            Inceptionsql = self.GenerateStatements(
                sql=sql,
                types='--enable-execute',
                backup='--disable-remote-backup')
        with self.con.cursor() as cursor:
            cursor.execute(Inceptionsql)
            result = cursor.fetchall()
            Dataset = [
                {
                    'ID': row[0],
                    'stage': row[1],
                    'errlevel': row[2],
                    'stagestatus': row[3],
                    'errormessage': row[4],
                    'sql': row[5],
                    'affected_rows': row[6],
                    'sequence': row[7],
                    'backup_dbname': row[8],
                    'execute_time': row[9],
                    'SQLSHA1': row[10]
                }
                for row in result
            ]
        return Dataset

    def Check(self, sql=None):
        Inceptionsql = self.GenerateStatements(sql=sql, types='--enable-check')
        ("out--", Inceptionsql)
        con = pymysql.connect(host=self.host,
                              user=self.user,
                              passwd=self.passwd,
                              port=6669,
                              db='',
                              charset="utf8")
        with con.cursor() as cursor:
            cursor.execute(Inceptionsql)
            result = cursor.fetchall()
            Dataset = [
                {
                    'ID': row[0],
                    'stage': row[1],
                    'errlevel': row[2],
                    'stagestatus': row[3],
                    'errormessage': row[4],
                    'sql': row[5],
                    'affected_rows': row[6],
                    'SQLSHA1': row[10]
                }
                for row in result
            ]
        return Dataset

    def oscstep(self, sql=None):
        with self.con.cursor(cursor=pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            cursor.close()
        return result

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    @staticmethod
    def BeautifySQL(sql):
        return sqlparse.format(sql, reindent=True, keyword_case='upper')

    def __str__(self):
        return '''

        InceptionSQL Class

        '''


if __name__ == '__main__':
    info = {
        'host': "172.16.130.202",
        'user': "applist",
        'password': "Fs9006",
        'db': "applist",
        'port': 3306
    }
    sql1 = 'UPDATE core_account SET email="teccccst@qq.com" WHERE username="liziyang";\nUPDATE core_account SET email="xddddieyifan@qq.com" WHERE username="test";;\n'
    sql = "UPDATE core_account SET email='teccccst@qq.com' WHERE username='liziyang';"
    # sql = str(sql).strip('\n').strip().rstrip(';')
    (sql)
    In = Inception(info)
    (In.Check(sql))
