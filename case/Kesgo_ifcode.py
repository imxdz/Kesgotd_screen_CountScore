import requests
import random
import json
import time
import pymssql
import random
from common.Mssql_pub import MssqlUtil
from common.Generate_Random import *
import sys
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from random import choice





class ScreenOperationOne():
 def __init__(self, s,base_url,mb,exname):
       # s = requests.session()  # 全局参数
       self.s = s
       self.base_url = base_url
       self.A = MssqlUtil()
       sql1 = "select a.ExperimentID,a.CaseID from dbo.AFCS_Experiment a join dbo.AFCS_TeacherInfo b " \
           "on a.AddUser = b.TeacherID " \
           "where MobileNo = '"+mb+"' " \
           "and ExperimentName = '"+exname+"' " \
           "and ExperimentStatus = '1'"
       B1 = self.A.mssql_getrows(sql1)   #根据教师手机号、实验名找该教师下已开始的实验id、案例id
       self.ExperimentID1 = str(B1[0][0])
       self.CaseID1 = str(B1[0][1])
       sql2 = "SELECT ClassID FROM dbo.AFCS_ClassSelect where ExperimentID ='"+self.ExperimentID1+"'"
       B2 = self.A.mssql_getrows(sql2)  #根据教师实验id找实验下的班级id 取第1个班级
       self.ClassID2 = str(B2[0][0])
       sql3 = "select QuestionsID,QuestionsContent,QuestionOrderNo from   dbo.AFCS_PolicyCaseQuestions where CaseID = '"+self.CaseID1+"' and QuestionType='1'"
       sql3s = "select * from   dbo.AFCS_PolicyCaseQuestions where CaseID = '"+self.CaseID1+"' and QuestionType='2'"
       B3 = self.A.mssql_getrows(sql3) #根据案例id找思考题id (简答题)
       B3s = self.A.mssql_getrows(sql3s) #根据案例id找思考题id (选择题)
       self.QuestionsID3 = str(B3[0][0])
       self.QuestionsContent3 = str(B3[0][1])
       self.QuestionOrderNo3 = str(B3[0][2])
       self.QuestionsID3s = str(B3s[0][0])
       self.QuestionsContent3s = str(B3s[0][1])
       self.QuestionOrderNo3s =  str(B3s[0][2])
       sql4 = "select StudentID FROM  dbo.AFCS_ClassStudents where ClassID = '"+self.ClassID2+"'"
       B4 = self.A.mssql_getrows(sql4) #根据班级id找学生id 取第一个学生
       self.StuLen = len(B4)
       self.StuList = B4
       self.StudentID4 = str(B4[0][0])
       self.RanStu = str(choice(self.StuList)[0])

 def Random_StuSelone(self):#随机抽取一个学生
    liststu = self.StuList
    RanStu = str(choice(liststu)[0])
    return RanStu

 def Random_StuSel(self,n):#随机取n个学生
    liststu = self.StuList
    slice = random.sample(liststu, n)
    return slice

 def WriteQuestion(self,stu):
#填写思考题（问答题）
     url = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/AddOrUpdateQuestionPreview")
     #url = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/AddOrUpdateQuestionPreview"
     body = {"questionpreviewinfo":
     "{\"QuestionsID\":\""+self.QuestionsID3+"\","
     "\"QuestionsContent\":\""+self.QuestionsContent3+"\","
     "\"CaseID\":\""+self.CaseID1+"\","
     "\"QuestionOrderNo\":"+self.QuestionOrderNo3+","
     "\"QuestionType\":1,"
     #"\"PreviewID\":\"280b969f-08be-439e-9f75-19500545598d\","
     "\"PreviewID\":\"00000000-0000-0000-0000-000000000000\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"PreviewContent\":\""+Generate(random.randint(1,20))+"\","
     "\"StudentID\":\""+stu+"\","
     "\"AddTime\":\"/Date(-62135596800000)/\","
     "\"Grade\":0,"
     "\"IsSubmit\":2,"
     "\"CaseQuesOption\":\"[]\","
     "\"PicList\":\"[]\"}"}
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r = self.s.post(url, json=body, headers=h)
     # print(r.status_code)

 # def GetPreviewID(self):
 #     url3 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/GetQuesByWhere"
     url3 = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/GetQuesByWhere")
     par = {"expID":self.ExperimentID1,
            "stuID":stu
            }
     h3= {"Accept": "application/json, text/plain, */*",
     "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
         }
     r3 = requests.get(url3,params=par,headers=h3)
     # print(r3.content.decode("utf-8"))
     a = r3.json()
     b = json.loads(a)
     c= b["Table"]
     for i in c:
         idt = dict(i)
         if idt["QuestionsID"]==self.QuestionsID3:
            d = idt["PreviewID"]
            # return d


 # def SubmitQuestion(self,d):
#提交思考题
     # url2 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/SaveQuesAnswer"
     url2 = urljoin(self.base_url,"kesgo.Service/wcf/CaseService.svc/SaveQuesAnswer")
     body2 = {"previewInfo":
     "[{\"PreviewID\":\""+d+"\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3+"\","
     "\"StudentID\":\""+stu+"\","
     "\"IsSubmit\":1},"
     "{\"PreviewID\":\"00000000-0000-0000-0000-000000000000\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3s+"\","
     "\"StudentID\":\""+stu+"\","
     "\"IsSubmit\":1}]"
            }
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r2 = self.s.post(url2, json=body2, headers=h)
     # print(r2.status_code)


class ScreenOperationTmp():
 def __init__(self,ExperimentID):
       self.A = MssqlUtil()
       sqlselgroup = "select GroupID from dbo.AFCS_Group where ExperimentID ='"+ExperimentID+"'"
       Bselgroup = self.A.mssql_getrows(sqlselgroup)
       self.Groupidlist = Bselgroup
 def JoinGroup(self,groupId,studentId):#观点分组
       # url = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/JoinGroup"  # 问号前面的
       url = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/JoinGroup")
       par = {
             "groupId":groupId,
             "studentId":studentId
             }
       h =  {
            "User-Agent":"Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36",
            "Accept": "application/json, text/plain, */*"
       }
       r = requests.get(url, params=par, headers=h)
       # print(r.text)
       # print(r.status_code)


class ScreenOperationTwo(ScreenOperationOne):
 def __init__(self,s,base_url,mb,exname):
#分组后发送观点讨论的组长发言
    super().__init__(s,base_url,mb,exname)
    sql5 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,GroupAnotherName,RealName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID join dbo.AFCS_StudentInfo c on b.StudentID = c.StudentID where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'"
    B5 = self.A.mssql_getrows(sql5) #根据实验id找小组组号、组长学生id 取第一个小组
    # print(B5)
    sql6 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"'"
    B6 = self.A.mssql_getrows(sql6)
    self.GroupID5 = str(B5[0][0])
    self.StudentID5 = str(B5[0][1])
    self.GroupOrderNo5 = str(B5[0][2])
    self.GroupName5 = str(B5[0][3])
    self.toGroupID5 = str(B5[1][0])
    self.toStudentID5 = str(B5[1][1])
    self.toGroupOrderNo5 = str(B5[1][2])
    self.toGroupName5 = str(B5[1][3])
    self.GroupStuList = B5
    self.GroupStuLen = len( B5)
    self.RanGroupStu = str(choice(self.GroupStuList)[1])
    self.Alist = B6
    self.Alen = len(B6)
    self.a = str(choice(self.Alist)[1])


 def Random_GroupStuSelone(self):
    listgroupstu = self.GroupStuList
    RanGroupStu = str(choice(listgroupstu)[1])
    return RanGroupStu

 def Random_GroupStuSel(self,n):#随机取n个组长
    listGroupstu = self.GroupStuList
    Groupslice = random.sample(listGroupstu, n)
    return Groupslice

 def Random_ASel(self,n):#随机取n个学生
    listA = self.Alist
    Aslice = random.sample(listA, n)
    return Aslice

 def TLGruopleaderSpeak(self,GroupID,groupstu,groupOrderNo,groupName,GroupAnotherName,RealName):
#观点讨论组长发言
    speakcontent = Unicode(random.randint(1,20))
    # url4 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateSpeak"
    url4 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateSpeak")
    body4 = {"speakEntity":
             "{\"SpeakID\":\"00000000-0000-0000-0000-000000000000\","
             "\"GroupID\":\""+GroupID+"\","
             "\"SpeakContent\":\""+speakcontent+"\","
             "\"Grade\":0,"
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"GroupOrderNo\":\""+groupOrderNo+"\","
             "\"NowStage\":1,"     #1是观点讨论  2是诊断总结
             "\"GroupName\":\""+groupName+"\","
             "\"StudentID\":\""+groupstu+"\","
             "\"IsDelete\":2,"
             "\"AddTime\":\"1900-1-1\"}"}
    h4 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    r4 = self.s.post(url4, json=body4, headers=h4)
    speakid = r4.text
    speakid = speakid.replace("\"", "")#去除双引号
#调组长发言siglar接口
    url4siglar = "http://192.168.0.249:18199/signalr/signalr/send?transport=longPolling&connectionToken=AQAAANCMnd8BFdERjHoAwE%2FCl%2BsBAAAAVdYmo0qzSEea%2BwEs7MZ4ngAAAAACAAAAAAAQZgAAAAEAACAAAACbjmTwtkJkk8GDojPJQGpqfhcTAPDRZJqbezvJCXP5lgAAAAAOgAAAAAIAACAAAAAAEr1ZVRi7Ly8wB3BXLlWhXvotbIoVE6jpC1g6V8nyTTAAAAD97qmwL2e9MY5QXQLaSmf5fxtHbPb%2FJiLghBIJ%2By7VvRb7hFjWjuZnR62JAdGqC5lAAAAAf7iRnrZhW02zWwAswZnpnXuCXs6gXsSDfgZLu3VYxQOlo3Dis61R%2F2%2FczYbeefYA9IGtlZBlSsDR2lgXySwE0w%3D%3D&groupid="+self.ExperimentID1
    body4siglar = {"data":"{\"H\":\"kesgohub\",\"M\":\"sendGroupSpeakData\",\"A\":[1,\"{\\\"speakID\\\":\\\""+speakid+"\\\",\\\"groupOrderNo\\\":\\\""+groupOrderNo+"\\\",\\\"groupName\\\":\\\""+groupName+"\\\",\\\"speakContent\\\":\\\""+speakcontent+"\\\",\\\"groupID\\\":\\\""+GroupID+"\\\",\\\"isLeader\\\":\\\"1\\\",\\\"studentId\\\":\\\""+groupstu+"\\\",\\\"realName\\\":\\\""+RealName+"\\\",\\\"headImage\\\":\\\"/images/common/normalFace.png\\\",\\\"groupAnotherName\\\":\\\""+GroupAnotherName+"\\\"}\"],\"I\":1}"}
    h4siglar = {"Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
           "User-Agent":"Mozilla/5.0 (Linux; Android 8.1.0; MI 8 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36"}
    r = requests.post(url4siglar, data=body4siglar, headers=h4siglar)

 def TLInteractionSpeak(self,stu):
#观点讨论我的互动
    # url5 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateTimeInteraction"
    url5 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateTimeInteraction")
    body5 = {"timeInteractionEntity":
             "{\"TimeInteractionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"InteractionContent\":\""+Unicode(random.randint(1,20))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"NowStage\":1,"
             "\"StudentID\":\""+stu+"\","
             "\"AddTime\":\"1900-1-1\"}"}
    h5 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    r5 = self.s.post(url5, json=body5, headers=h5)



 def AaskB(self,GroupID,GroupName,toGroupID,toGroupName,StudentID,GroupOrderNo):
#组间博弈提问A→B
    # url6 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAsk"
    url6 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateAsk")
    body6 = {"askEntity":
             "{\"AskQuestionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"AskGroupID\":\""+GroupID+"\","
             "\"AskGroupName\":\""+GroupName+"\","
             "\"ToAskGroupID\":\""+toGroupID+"\","
             "\"ToAskGroupName\":\""+toGroupName+"\","
             "\"QuestionContent\":\""+Unicode(random.randint(1,20))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"StudentID\":\""+StudentID+"\","
             "\"AddTime\":\"2017-03-14\","
             "\"GroupOrderNo\":"+GroupOrderNo+","
             "\"Grade\":0,"
             "\"IsDelete\":2}"}
    h6 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    r6 = self.s.post(url6, json=body6, headers=h6)
    AskQuestionIDA_B = r6.text
    return  AskQuestionIDA_B

 def BaskA(self):
#组间博弈提问B→A
    # url61 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAsk"
    url61 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateAsk")
    h61 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    body61 = {"askEntity":
             "{\"AskQuestionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"AskGroupID\":\""+self.toGroupID5+"\","
             "\"AskGroupName\":\""+self.toGroupName5+"\","
             "\"ToAskGroupID\":\""+self.GroupID5+"\","
             "\"ToAskGroupName\":\""+self.GroupName5+"\","
             "\"QuestionContent\":\""+Unicode(random.randint(1,20))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"StudentID\":\""+self.toStudentID5+"\","
             "\"AddTime\":\"2017-03-14\","
             "\"GroupOrderNo\":"+self.toGroupOrderNo5+","
             "\"Grade\":0,"
             "\"IsDelete\":2}"}
    r61 = self.s.post(url61, json=body61, headers=h61)
    # print(r61.text) # AskQuestionID
    AskQuestionIDB_A = r61.text
    # print(r61.text)
    # print(r61.status_code)
    return AskQuestionIDB_A


#一定点击开始回答按钮!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#AskQuestionIDB_A = "82A08B5F-5627-4BAA-97EC-68AD6C94E91C"
#组间博弈回答A回答
 def Aanswer(self,AskQuestionID,StudentID,GroupID,GroupName,GroupOrderNo):
    # url7 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAnswer"
    url7 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateAnswer")
    body7 ={"answerEntity":
            "{\"AnswerID\":\"00000000-0000-0000-0000-000000000000\","
            "\"AnswerrGroupID\":\"00000000-0000-0000-0000-000000000000\","
            #"\"AskQuestionID\":\"BA42AFB6-0399-4C94-AEDA-9F96BB4E148F\","
            "\"AskQuestionID\":"+AskQuestionID+","
            "\"AnswerContent\":\""+Unicode(random.randint(1,20))+"\","
            "\"AddTime\":\"2017-01-01\","
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"StudentID\":\""+StudentID+"\","
            "\"GroupID\":\""+GroupID+"\","
            "\"GroupName\":\""+GroupName+"\","
            "\"GroupOrderNo\":\""+GroupOrderNo+"\","
            "\"Grade\":0,"
            "\"IsDelete\":2,"
            "\"IsLeader\":true}"}
    h7 = {
    "Connection": "keep-alive",
    "Content-Length": "521",
    "Accept": "application/json, text/plain, */*",
    "Origin": "null",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.8",
    "X-Requested-With":"com.allpass.kesgo"
     }
    r7 = self.s.post(url7, json=body7, headers=h7)


 def Banswer(self,AskQuestionIDA_B):
#组间博弈回答B回答
    # url8 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAnswer"
    url8 = urljoin(self.base_url,"kesgo.Service/wcf/DiscussionService.svc/CreateAnswer")
    body8 ={"answerEntity":
            "{\"AnswerID\":\"00000000-0000-0000-0000-000000000000\","
            "\"AnswerrGroupID\":\"00000000-0000-0000-0000-000000000000\","
            #"\"AskQuestionID\":\"BA42AFB6-0399-4C94-AEDA-9F96BB4E148F\","
            "\"AskQuestionID\":"+AskQuestionIDA_B+","
            "\"AnswerContent\":\""+Unicode(random.randint(1,20))+"\","
            "\"AddTime\":\"2017-01-01\","
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"StudentID\":\""+self.toStudentID5+"\","
            "\"GroupID\":\""+self.toGroupID5+"\","
            "\"GroupName\":\""+self.toGroupName5+"\","
            "\"GroupOrderNo\":\""+self.toGroupOrderNo5+"\","
            "\"Grade\":0,"
            "\"IsDelete\":2,"
            "\"IsLeader\":true}"}
    h8 = {
    "Connection": "keep-alive",
    "Content-Length": "521",
    "Accept": "application/json, text/plain, */*",
    "Origin": "null",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.8",
    "X-Requested-With":"com.allpass.kesgo"
     }
    r8 = self.s.post(url8, json=body8, headers=h8)


 def ZDGruopleaderSpeak(self,GroupID,GroupOrderNo,GroupName,StudentID):
#诊断总结组长发言
    # url9 = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData"
    url9 = urljoin(self.base_url,"kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData")
    body9 = {"speakInfo":
            "{\"GroupID\":\""+GroupID+"\","
            "\"SpeakContent\":\""+Unicode(random.randint(1,20))+"\","
            "\"Grade\":0,"
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"GroupOrderNo\":\""+GroupOrderNo+"\","
            "\"NowStage\":2,"
            "\"GroupName\":\""+GroupName+"\","
            "\"StudentID\":\""+StudentID+"\","
            "\"IsDelete\":2,"
            "\"IsSendSpeak\":2,"
            "\"IsView\":2}"}
    h9 = {
    "Connection": "keep-alive",
    "Content-Length": "521",
    "Accept": "application/json, text/plain, */*",
    "Origin": "null",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.8",
    "X-Requested-With":"com.allpass.kesgo"
     }
    r9 = self.s.post(url9, json=body9, headers=h9)


 def ZDInteractionSpeak(self,GroupID,GroupOrderNo,GroupName,StudentID):
#诊断总结我的互动
    # url10 = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData"
    url10 = urljoin(self.base_url,"kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData")
    body10 ={"speakInfo":
            "{\"GroupID\":\""+GroupID+"\","
            "\"SpeakContent\":\""+Unicode(random.randint(1,20))+"\","
            "\"Grade\":0,"
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"GroupOrderNo\":\""+GroupOrderNo+"\","
            "\"NowStage\":2,"
            "\"GroupName\":\""+GroupName+"\","
            "\"StudentID\":\""+StudentID+"\","
            "\"IsDelete\":2,"
            "\"IsSendSpeak\":2,"
            "\"IsView\":3}"}
    h10 = {
    "Connection": "keep-alive",
    "Content-Length": "521",
    "Accept": "application/json, text/plain, */*",
    "Origin": "null",
    "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.8",
    "X-Requested-With":"com.allpass.kesgo"
     }
    r10 = self.s.post(url10, json=body10, headers=h10)


 def Groupvote(self,StudentID,toGroupID):
#小组投票
    # url11 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/InsertGroupEvaluation"
    url11 = urljoin(self.base_url,"kesgo.Service/wcf/CoursePerformService.svc/InsertGroupEvaluation")
    par11 = {"stuID":StudentID,
         "groupID":toGroupID }
    h11 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r11 = self.s.get(url11,params=par11,headers=h11)


 def Personalvote(self,StudentID,toStudentID):
#个人投票
    # url12 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/AddStudentVote"
    url12 = urljoin(self.base_url,"kesgo.Service/wcf/CoursePerformService.svc/AddStudentVote")
    par12 = {"expID":self.ExperimentID1,
         "stuID":StudentID,
         "excellenceID":toStudentID }
    h12 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r12 = self.s.get(url12,params=par12,headers=h12)


 def Closeconn(self):
     self.A.mssql_close()






if __name__ == "__main__":
    base_url = "http://192.168.0.167"
    s = requests.session()
    mb = "18913938700"
    exname = "ert"
    interoperone = ScreenOperationOne(s,base_url,mb,exname)
    b = interoperone.RanStu
    bb = interoperone.Random_StuSel()
    bbb = interoperone.Random_StuSel()
    # print(b,bb,bbb)



