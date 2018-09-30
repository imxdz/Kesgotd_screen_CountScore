# coding:utf-8
import unittest
import ddt
import os
from common import readexcel
from common import writeexcel
from common.Mssql_pub import MssqlUtil
from config import readConfig

# 获取write.xlsx路径
curpath = os.path.dirname(os.path.realpath(__file__))
testxlsx = os.path.join(curpath, "write.xlsx")
testdata = readexcel.Excelread(testxlsx).dict_data()
experimentname  = readConfig.exname
@ddt.ddt
class Test_api(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.A = MssqlUtil()
        # sql = "select StudentID from dbo.AFCS_GroupStudents where StudentID ='"+!!+"'"
        # sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = 'cccttt'"
        # cls.list= cls.A.mssql_getrows(sql)

    @ddt.data(*testdata)
    def test_totalscore(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("总分是%s"%data["总分"],"库里总分是%s"%float(str(stulist[0][14])))
        self.assertTrue(abs(data["总分"] - float(str(stulist[0][14])))<0.01)

    @ddt.data(*testdata)
    def test_classdiscuss(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("课堂讨论是%s"%data["课堂讨论"],"库里课堂讨论是%s"%float(str(stulist[0][6])))
        self.assertTrue(abs(data["课堂讨论"] - float(str(stulist[0][6])))<0.01)

    @ddt.data(*testdata)
    def test_groupperform(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("小组表现是%s"%data["小组表现"],"库里小组表现是%s"%float(str(stulist[0][13])))
        self.assertTrue(abs(data["小组表现"] - float(str(stulist[0][13])))<0.01)

    @ddt.data(*testdata)
    def test_personalperform(self, data):
        stuid = data["学生id"]
        sql = "select * from dbo.AFCS_StudentScore a join dbo.AFCS_Experiment b on a.ExperimentID = b.ExperimentID where ExperimentName = '"+experimentname+"' and StudentID = '"+stuid+"'"
        stulist= self.A.mssql_getrows(sql)
        print("个人表现是%s"%data["个人表现"],"库里个人表现是%s"%float(str(stulist[0][10])))
        self.assertTrue(abs(data["个人表现"] - float(str(stulist[0][10])))<0.01)
if __name__ == "__main__":
    unittest.main()
