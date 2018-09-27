# coding:utf-8
import pymssql


mssql_info = {"host":'192.168.0.167\SQL2008',
               "user":'kesgo',
               "passwd":'kesgo',
               "db":'kesgo',
               "charset":'utf8'}

class MssqlUtil():

    def __init__(self):
        self.db_info = mssql_info
        u'''连接池方式'''
        self.conn = MssqlUtil.__getConnect(self.db_info)

    @staticmethod
    def __getConnect(db_info):
        try:
            conn = pymssql.connect(host=db_info['host'],
                                   user=db_info['user'],
                                   password=db_info['passwd'],
                                   database=db_info['db'],
                                   charset=db_info['charset'])
            return conn
        except Exception as a:
            print("数据库连接异常：%s"%a)

    def mssql_execute(self, sql):
        '''执行sql语句'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            self.conn.rollback()         # sql执行异常后回滚
            print("执行SQL语句出现异常：%s"%a)
        else:
            cur.close()
            self.conn.commit()          # sql无异常时提交

    def mssql_getrows(self, sql):
        ''' 返回查询结果'''
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as a:
            print("执行SQL语句出现异常：%s"%a)
        else:
            rows = cur.fetchall()
            cur.close()
            # rows为二维元祖 eg：(('id','title'),) 或(('id1','title1'),('id2','title2'))
            return rows

    def mssql_getstring(self, sql):
        '''查询某个字段的对应值'''
        rows = self.mssql_getrows(sql)
        if rows != None:
            for row in rows:
                for i in row:
                    return i

    def mssql_close(self):
        ''' 关闭 close mysql'''
        try:
            self.conn.close()
        except Exception as a:
            print("数据库关闭时异常：%s"%a)
if __name__ == "__main__":
    A = MssqlUtil()
    # sql = "select ClassSelectID from AFCS_ClassSelect where ExperimentID = '37494CCC-6123-4F0E-9D42-D1226FA8CFE9'AND ClassSelectID = '9e6854af-f0c7-4703-b677-00918d8daf7c' "
    # # B = A.mssql_getrows(sql)
    # print(B)
    # a1 = B[0]
    # print(a1)
    # a2 = a1[0]  #实验下班级ID
    # print(a2)
    # A.mssql_close()
    from config import readConfig
    from common import readexcel
    testxlsx = ("C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx")
    a = readConfig.exname
    print(a)
    testdata = readexcel.Excelread(testxlsx).dict_data()
    stuid = testdata[0]["学生id"]
    print(stuid)
    sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+a+"' and StudentID = '"+stuid+"'"
    stulist= A.mssql_getrows(sql)
    b = testdata[0]["总分"] == float(str(stulist[0][14]))
    print(b)



