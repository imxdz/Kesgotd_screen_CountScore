import requests
import random
import json
import time
import pymssql
import random
from common.Mssql_pub import MssqlUtil
import sys
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin


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
       self.StudentID4 = str(B4[0][0])


 def WriteQuestion(self):
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
     "\"PreviewContent\":\""+str(random.randint(1,1000))+"\","
     "\"StudentID\":\""+self.StudentID4+"\","
     "\"AddTime\":\"/Date(-62135596800000)/\","
     "\"Grade\":0,"
     "\"IsSubmit\":2,"
     "\"CaseQuesOption\":\"[]\","
     "\"PicList\":\"[]\"}"}
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r = self.s.post(url, json=body, headers=h)
     print(r.status_code)

 def GetPreviewID(self):
     url3 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/GetQuesByWhere"
     par = {"expID":self.ExperimentID1,
            "stuID":self.StudentID4
            }
     h3= {"Accept": "application/json, text/plain, */*",
     "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
         }
     r3 = requests.get(url3,params=par,headers=h3)
     print(r3.content.decode("utf-8"))
     a = r3.json()
     b = json.loads(a)
     c= b["Table"]
     for i in c:
         idt = dict(i)
         if idt["QuestionsID"]==self.QuestionsID3:
            d = idt["PreviewID"]
            return d


 def SubmitQuestion(self,d):
#提交思考题
     url2 = "http://192.168.0.167/kesgo.Service/wcf/CaseService.svc/SaveQuesAnswer"
     body2 = {"previewInfo":
     "[{\"PreviewID\":\""+d+"\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3+"\","
     "\"StudentID\":\""+self.StudentID4+"\","
     "\"IsSubmit\":1},"
     "{\"PreviewID\":\"00000000-0000-0000-0000-000000000000\","
     "\"ExperimentID\":\""+self.ExperimentID1+"\","
     "\"QuestionsID\":\""+self.QuestionsID3s+"\","
     "\"StudentID\":\""+self.StudentID4+"\","
     "\"IsSubmit\":1}]"
            }
     h = {"Content-Type": "application/json;charset=UTF-8"}
     r2 = self.s.post(url2, json=body2, headers=h)
     print(r2.status_code)



class ScreenOperationTwo(ScreenOperationOne):
 def __init__(self,s,base_url,mb,exname):
#分组后发送观点讨论的组长发言
    super().__init__(s,base_url,mb,exname)
    sql5 = "select a.GroupID,b.StudentID,a.GroupOrderNo,GroupName,* from dbo.AFCS_Group a join dbo.AFCS_GroupStudents b on a.GroupID = b.GroupID " \
       "where a.ExperimentID = '"+self.ExperimentID1+"' and b.IsLeader = '1'"
    B5 = self.A.mssql_getrows(sql5) #根据实验id找小组组号、组长学生id 取第一个小组
    self.GroupID5 = str(B5[0][0])
    self.StudentID5 = str(B5[0][1])
    self.GroupOrderNo5 = str(B5[0][2])
    self.GroupName5 = str(B5[0][3])
    self.toGroupID5 = str(B5[1][0])
    self.toStudentID5 = str(B5[1][1])
    self.toGroupOrderNo5 = str(B5[1][2])
    self.toGroupName5 = str(B5[1][3])


 def TLGruopleaderSpeak(self):
#观点讨论组长发言
    url4 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateSpeak"
    body4 = {"speakEntity":
             "{\"SpeakID\":\"00000000-0000-0000-0000-000000000000\","
             "\"GroupID\":\""+self.GroupID5+"\","
             "\"SpeakContent\":\""+str(random.randint(1,1000))+"\","
             "\"Grade\":0,"
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"GroupOrderNo\":\""+self.GroupOrderNo5+"\","
             "\"NowStage\":1,"     #1是观点讨论  2是诊断总结
             "\"GroupName\":\""+self.GroupName5+"\","
             "\"StudentID\":\""+self.StudentID5+"\","
             "\"IsDelete\":2,"
             "\"AddTime\":\"1900-1-1\"}"}
    h4 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    r4 = self.s.post(url4, json=body4, headers=h4)


 def TLInteractionSpeak(self):
#观点讨论我的互动
    url5 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateTimeInteraction"
    body5 = {"timeInteractionEntity":
             "{\"TimeInteractionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"InteractionContent\":\""+str(random.randint(1,1000))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"NowStage\":1,"
             "\"StudentID\":\""+self.StudentID5+"\","
             "\"AddTime\":\"1900-1-1\"}"}
    h5 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    r5 = self.s.post(url5, json=body5, headers=h5)



 def AaskB(self):
#组间博弈提问A→B
    url6 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAsk"
    body6 = {"askEntity":
             "{\"AskQuestionID\":\"00000000-0000-0000-0000-000000000000\","
             "\"AskGroupID\":\""+self.GroupID5+"\","
             "\"AskGroupName\":\""+self.GroupName5+"\","
             "\"ToAskGroupID\":\""+self.toGroupID5+"\","
             "\"ToAskGroupName\":\""+self.toGroupName5+"\","
             "\"QuestionContent\":\""+str(random.randint(1,1000))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"StudentID\":\""+self.StudentID5+"\","
             "\"AddTime\":\"2017-03-14\","
             "\"GroupOrderNo\":"+self.GroupOrderNo5+","
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
    url61 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAsk"
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
             "\"QuestionContent\":\""+str(random.randint(1,1000))+"\","
             "\"ExperimentID\":\""+self.ExperimentID1+"\","
             "\"StudentID\":\""+self.toStudentID5+"\","
             "\"AddTime\":\"2017-03-14\","
             "\"GroupOrderNo\":"+self.toGroupOrderNo5+","
             "\"Grade\":0,"
             "\"IsDelete\":2}"}
    r61 = self.s.post(url61, json=body61, headers=h61)
    #print(r61.text) # AskQuestionID
    AskQuestionIDB_A = r61.text
    print(r61.text)
    print(r61.status_code)
    return AskQuestionIDB_A


#一定点击开始回答按钮!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


#AskQuestionIDB_A = "82A08B5F-5627-4BAA-97EC-68AD6C94E91C"
#组间博弈回答A回答
 def Aanswer(self,AskQuestionIDB_A):
    url7 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAnswer"
    body7 ={"answerEntity":
            "{\"AnswerID\":\"00000000-0000-0000-0000-000000000000\","
            "\"AnswerrGroupID\":\"00000000-0000-0000-0000-000000000000\","
            #"\"AskQuestionID\":\"BA42AFB6-0399-4C94-AEDA-9F96BB4E148F\","
            "\"AskQuestionID\":"+AskQuestionIDB_A+","
            "\"AnswerContent\":\""+str(random.randint(1,1000))+"\","
            "\"AddTime\":\"2017-01-01\","
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"StudentID\":\""+self.StudentID5+"\","
            "\"GroupID\":\""+self.GroupID5+"\","
            "\"GroupName\":\""+self.GroupName5+"\","
            "\"GroupOrderNo\":\""+self.GroupOrderNo5+"\","
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
    url8 = "http://192.168.0.167/kesgo.Service/wcf/DiscussionService.svc/CreateAnswer"
    body8 ={"answerEntity":
            "{\"AnswerID\":\"00000000-0000-0000-0000-000000000000\","
            "\"AnswerrGroupID\":\"00000000-0000-0000-0000-000000000000\","
            #"\"AskQuestionID\":\"BA42AFB6-0399-4C94-AEDA-9F96BB4E148F\","
            "\"AskQuestionID\":"+AskQuestionIDA_B+","
            "\"AnswerContent\":\""+str(random.randint(1,1000))+"\","
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


 def ZDGruopleaderSpeak(self):
#诊断总结组长发言
    url9 = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData"
    body9 = {"speakInfo":
            "{\"GroupID\":\""+self.GroupID5+"\","
            "\"SpeakContent\":\""+str(random.randint(1,1000))+"\","
            "\"Grade\":0,"
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"GroupOrderNo\":\""+self.GroupOrderNo5+"\","
            "\"NowStage\":2,"
            "\"GroupName\":\""+self.GroupName5+"\","
            "\"StudentID\":\""+self.StudentID5+"\","
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


 def ZDInteractionSpeak(self):
#诊断总结我的互动
    url10 = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SaveSpeakData"
    body10 ={"speakInfo":
            "{\"GroupID\":\""+self.GroupID5+"\","
            "\"SpeakContent\":\""+str(random.randint(1,1000))+"\","
            "\"Grade\":0,"
            "\"ExperimentID\":\""+self.ExperimentID1+"\","
            "\"GroupOrderNo\":\""+self.GroupOrderNo5+"\","
            "\"NowStage\":2,"
            "\"GroupName\":\""+self.GroupName5+"\","
            "\"StudentID\":\""+self.StudentID5+"\","
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


 def Groupvote(self):
#小组投票
    url11 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/InsertGroupEvaluation"
    par11 = {"stuID":self.StudentID5,
         "groupID":self.toGroupID5 }
    h11 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r11 = self.s.get(url11,params=par11,headers=h11)


 def Personalvote(self):
#个人投票
    url12 = "http://192.168.0.167/kesgo.Service/wcf/CoursePerformService.svc/AddStudentVote"
    par12 = {"expID":self.ExperimentID1,
         "stuID":self.StudentID5,
         "excellenceID":self.toStudentID5 }
    h12 = {
         "Accept": "application/json, text/plain, */*",
         "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36"
      }
    r12 = self.s.get(url12,params=par12,headers=h12)


 def Closeconn(self):
     self.A.mssql_close()



if __name__ == "__main__":
    mb = '12345678922'
    exname = 'test0601'





