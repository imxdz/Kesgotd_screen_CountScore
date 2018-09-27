from operator import itemgetter, attrgetter
from common.Mssql_pub import MssqlUtil
class Score():
 def __init__(self):
    self.A = MssqlUtil()

 # def getscore(self,a,b):#取实际评分（评星）
 #        aa = []
 #        scored = {}
 #        for i in b:
 #            if aa.count(i)%2==1:
 #                for key,value in i.items():
 #                    stuid = a[-key]
 #                    defen = value-1
 #                    scored[stuid]=defen
 #            else:
 #                for key,value in i.items():
 #                    stuid = a[-key]
 #                    defen = value
 #                    scored[stuid]=defen
 #            aa.append(i)
 #        return scored
 def getscore(self,a,b):#取实际评星（评星）
        scored = {}
        for i in b:
            for key,value in i.items():
                    stuid = a[-key]
                    if stuid in scored.keys() and value ==scored[stuid]:
                        scored[stuid]=value-1
                    else:
                        scored[stuid]=value
        return scored

 def getscore2(self,a,b):#取实际评分（拖动滚动条）
   bb=b[::-1]#列表反序
   ii = []
   scored = {}
   for i in bb:
       for key,value in i.items():
           # print(key,value)
           if key not in ii:
               stuid = a[-key]
               defen = value
               scored[stuid]=defen
               # print("学生%s评%s分"%(stuid,defen))
               ii.append(key)
   return scored

 def getPercent(self,a):#取百分比
   b = range(100,-5,-5)
   # print(b[20])
   sumspeak = []
   set_a = set(a) #List_set是另外一个列表，里面的内容是List里面的无重复 项
   # print(set_a)
   # print(type(set_a))
   for item in set_a:
     # print("the %s has found %d" %(item,a.count(item)))
     sumspeak.append((item,a.count(item)))
  # print(sumspeak)
   sumspeaksort = sorted(sumspeak, key=itemgetter(1), reverse=True)
  # print(sumspeaksort)
   len1 = len(sumspeaksort)#5
   grouppercents = [(sumspeaksort[0][0],100)]
   nextn = 1
   for i in  range(len1-1):#0开始到3
     if sumspeaksort[i][1]==sumspeaksort[i+1][1]:
         grouppercents.append((sumspeaksort[i+1][0],grouppercents[i][1]))
     else:
         grouppercents.append((sumspeaksort[i+1][0],b[i+1]))
   # print(grouppercents)
   return grouppercents

 def getsysscore(self,listcount,fz):#取系统得分（小组）
    scorelist = {}
    groupspercent = self.getPercent(listcount)
    # print(groupspercent)
    for grouppercent in groupspercent:
        # print(grouppercent)
        # print(type(grouppercent[0]))
        if type(grouppercent[0])== tuple:
            grouppercentid = grouppercent[0][0]
        else:
            grouppercentid = grouppercent[0]
        # print("小组id是%s"%grouppercentid)
        scoresql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+grouppercentid+"'"
        scoregetstulist= self.A.mssql_getrows(scoresql)
        for scoregetstu in scoregetstulist:
            scoreStudentID = str(scoregetstu[0])
            # print("学生id是%s"%scoreStudentID)
            stupercent = grouppercent[1]
            # print(type(stupercent))
            # print("百分比是%s"%stupercent)
            scorelist[scoreStudentID]=((stupercent)/100)*fz
    # print("学生得分%s"%scorelist)
    return scorelist

 def getsysscore2(self,listcount,fz):#取系统得分（个人）
    scorelist = {}
    groupspercent = self.getPercent(listcount)
    # print(groupspercent)
    for grouppercent in groupspercent:
        # print(grouppercent)
        # print(type(grouppercent[0]))
        if type(grouppercent[0])== tuple:
            grouppercentid = grouppercent[0][0]
        else:
            grouppercentid = grouppercent[0]
        # print("小组id是%s"%grouppercentid)
        scoresql = "select StudentID from dbo.AFCS_GroupStudents where StudentID ='"+grouppercentid+"'"
        scoregetstulist= self.A.mssql_getrows(scoresql)
        for scoregetstu in scoregetstulist:
            scoreStudentID = str(scoregetstu[0])
            # print("学生id是%s"%scoreStudentID)
            stupercent = grouppercent[1]
            # print(type(stupercent))
            # print("百分比是%s"%stupercent)
            scorelist[scoreStudentID]=((stupercent)/100)*fz
    # print("学生得分%s"%scorelist)
    return scorelist

 def gettecscored(self,listcount,listcountscored,fz):#取教师评分（评星）
    scoredlist = {}
    set_listcount = set(listcount)
    set_set_listcountsort = sorted(set_listcount, key=itemgetter(2), reverse=True)
    groupscored = self.getscore(set_set_listcountsort,listcountscored)
    # print(groupscored)
    for groupkey,groupvalue in groupscored.items():
        groupidscored = groupkey[0]
        # print("小组id是%s"%groupidscored)
        scoredsql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+groupidscored+"'"
        scoredgetstulist= self.A.mssql_getrows(scoredsql)
        for scoredgetstu in scoredgetstulist:
            scoredStudentID = str(scoredgetstu[0])
            # print("学生id是%s"%scoredStudentID)
            stuscored = groupvalue
            # print(type(stuscored))
            # print("星数是%s"%stuscored)
            scoredlist[scoredStudentID]=stuscored*fz
    # print("学生发言评分%s"%scoredlist)
    return scoredlist

 def gettecscored2(self,listcount,listcountscored,fz):#取教师评分（拖动滚动条）
    scoredlist = {}
    set_listcount = set(listcount)
    set_set_listcountsort = sorted(set_listcount, key=itemgetter(2), reverse=True)
    groupscored = self.getscore2(set_set_listcountsort,listcountscored)
    # print(groupscored)
    for groupkey,groupvalue in groupscored.items():
        groupidscored = groupkey[0]
        # print("小组id是%s"%groupidscored)
        scoredsql = "select StudentID from dbo.AFCS_GroupStudents where GroupID ='"+groupidscored+"'"
        scoredgetstulist= self.A.mssql_getrows(scoredsql)
        for scoredgetstu in scoredgetstulist:
            scoredStudentID = str(scoredgetstu[0])
            # print("学生id是%s"%scoredStudentID)
            stuscored = groupvalue
            # print(type(stuscored))
            # print("星数是%s"%stuscored)
            scoredlist[scoredStudentID]=stuscored*fz
    # print("学生发言评分%s"%scoredlist)
    return scoredlist

















if __name__ == '__main__':
    def getscore(a,b):
        scored = {}
        for i in b:
            for key,value in i.items():
                    stuid = a[-key]
                    if stuid in scored.keys() and value ==scored[stuid]:
                        scored[stuid]=value-1
                    else:
                        scored[stuid]=value
        return scored
    A = ['aaa','bbb','ccc','ddd','eee','fff','ggg','hhh','iii']#学生id

    a = ['aaa', 'ccc', 'eee', 'fff', 'ggg']#思考题提交的学生id 按时间顺序
    b = [{1:2},{1:2},{2:5},{2:4},{2:3},{3:1},{3:5},{1:1}]
    print(getscore(a,b))
    aaa = ()
    aaa[0]=1
    print(aaa)

    # score = Score()
    # a = [('95fee367-becc-447b-a8cc-a1bae882a4c2', 'c3', '3'),('95fee367-becc-447b-a8cc-a1bae882a4c2', 'c3', '3'),('95fee367-becc-447b-a8cc-a1bae882a4c2', 'c3', '3'),
    #    ('6dba682d-b7bf-44e3-a89e-bba71e17a378', 'e5', '5'),('6dba682d-b7bf-44e3-a89e-bba71e17a378', 'e5', '5'),('6dba682d-b7bf-44e3-a89e-bba71e17a378', 'e5', '5'),
    #      ('6dba682d-b7bf-44e3-a89e-bba71e17a378', 'e5', '5')]
    #
    # aaa = score.getsysscore(a,15)
    # print(aaa)

    # b = ['6dba682d-b7bf-44e3-a89e-bba71e17a378','6dba682d-b7bf-44e3-a89e-bba71e17a378']
    # bbb = score.getsysscore(b,10)
    # print(bbb)
    # l =[1, 2, [3, [4, 5, 6, [7, 8, [9, 10, [11, 12, 13, [14, 15,[16,[17,]],19]]]]]]]
    #
    # def search(l):
    #     for item in l:
    #         if type(item) is list:
    #             search(item)
    #         else:
    #             print(item)
    #
    # search(l)


