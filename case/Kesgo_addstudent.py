import requests
from flask import json
import string
import random
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from common.Generate_Random import *
#教师登录后，添加班级，在该班级下，添加并编辑9个手机号码随机、学号随机、QQ号、生日随机的学生
class Add_Student():
    def __init__(self,base_url):
       self.base_url = base_url

    def tec_login(self,loginName,loginPWD):
        tec_login_url = urljoin(self.base_url,"kesgo.Service/wcf/TeacherInfoService.svc/LoginIn")
        tec_login_par = {
            "v":"1534812768392",
            "loginName":loginName,
            "loginPWD":loginPWD
        }
        tec_login_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        tec_login_r = requests.get(tec_login_url, params=tec_login_par, headers=tec_login_h)
        res = tec_login_r.json()
        return res

    def gettecid(self,res):
        dict1 = json.loads(res)
        useid = dict1["UserID"]
        return useid

    def add_class(self,TeacherID,ClassName):
        add_class_url = urljoin(self.base_url,"kesgo.Service/wcf/TeacherInfoService.svc/CreateOrUpdateClass?v=1534813216483")
        #add_class_url= "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/CreateOrUpdateClass?v=1534813216483"
        add_class_json ={
            "classInfo": "{\"ClassID\":\"00000000-0000-0000-0000-000000000000\","
                         "\"TeacherID\":\""+TeacherID+"\","
                         "\"ClassName\":\""+ClassName+"\"}"
        }
        add_class_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        add_class_r = requests.post(add_class_url, json=add_class_json, headers=add_class_h)
        a = add_class_r.text
        return a

    def get_all_classid(self,teachId):
        get_all_classid_url = urljoin(self.base_url,"kesgo.Service/wcf/TeacherInfoService.svc/GetClassInfoByID")

        #get_all_classid_url = "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/GetClassInfoByID"
        get_all_classid_par={
            "v":"1534813217520",
            "teachId":teachId
        }
        get_all_classid_h = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        get_all_classid_r = requests.get(get_all_classid_url, params=get_all_classid_par, headers=get_all_classid_h)
        result3 = get_all_classid_r.content.decode("utf-8")
        return get_all_classid_r.json()

    def get_add_class_classId(self,allclassId,ClassName):
        str1=allclassId
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            # print(type(dict1))
            # print(dict1)
            if dict1["ClassName"]==ClassName:
                return (dict1["ClassID"])

    def add_stu(self,adduser,realname,password,phone,classId):
        add_stu_url = urljoin(self.base_url,"kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534814126452")
        #add_stu_url = "http://123.206.230.41:8080/kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534814126452"
        add_stu_json ={
            "stuInfo": "{\"adduser\":\""+adduser+"\",\"adduserrole\":1,\"realname\":\""+realname+"\",\"password\":\""+password+"\",\"phone\":\""+phone+"\",\"classId\":\""+classId+"\"}",
	        "classId": classId
        }
        add_stu_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        add_stu_r=requests.post(add_stu_url, json=add_stu_json, headers=add_stu_h)
        b = add_stu_r.text
        return b

    def get_all_stu(self,classID):
        get_all_stu_url = urljoin(self.base_url,"kesgo.Service/wcf/TeacherInfoService.svc/PageStuInfos")
        #get_all_stu_url = "http://123.206.230.41:8080/kesgo.Service/wcf/TeacherInfoService.svc/PageStuInfos"
        get_all_stu_par = {
            "v":"1534814127566",
            "searchText":"",
            "classID":classID,
            "pageIndex":"1",
            "pageSize":"10"
        }
        get_all_stu_h ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        get_all_stu_r=requests.get(get_all_stu_url, params=get_all_stu_par, headers=get_all_stu_h)
        return get_all_stu_r.json()

    def get_add_StudentID(self,allsutdentid,realname):
        str1=allsutdentid
        list1 = json.loads(str1)
        for i in list1:
            dict1 = dict(i)
            # print(type(dict1))
            # print(dict1)
            if dict1["RealName"] == realname:
                return (dict1["StudentID"])

    def edit_add_stu(self,adduser,realname,password,phone,studentnumber,qq,birthday,classId,studentID):
        edit_add_stu_url = urljoin(self.base_url,"kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534815539827")
        #edit_add_stu_url="http://123.206.230.41:8080/kesgo.Service/wcf/StudentInfoService.svc/AddorUpdateStudentInfo?v=1534815539827"
        edit_add_stu_json={
            	"stuInfo": "{\"adduser\":\""+adduser+"\",\"adduserrole\":1,\"realname\":\""+realname+"\",\"password\":\""+password+"\",\"phone\":\""+phone+"\",\"studentnumber\":\""+studentnumber+"\",\"qq\":\""+qq+"\",\"birthday\":\""+birthday+"\",\"classId\":\""+classId+"\",\"studentID\":\""+studentID+"\"}",
            	"classId": classId
        }
        edit_add_stu_h={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
        }
        edit_add_stu_r=requests.post(edit_add_stu_url, json=edit_add_stu_json, headers=edit_add_stu_h)

    def phone_num(self):
        num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
             '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
        start = random.choice(num_start)
        end = ''.join(random.sample(string.digits,7))
        res = start+end
        return res
    def stu_num(self):
        end = ''.join(random.sample(string.digits,5))
        return end
    def QQ_num(self):
        end = ''.join(random.sample(string.digits,7))
        return end
    def birthday(self):
        num_month = ['01-01', '02-01', '03-01', '04-01', '05-01', '06-01', '07-01', '08-01', '09-01', '10-01', '11-01', '12-01']
        return num_month

    def has_stu(self,mb,exname):
        res = self.tec_login(mb,"1")
        teacherid = self.gettecid(res)         #获取登录的教师id
        a = self.add_class(teacherid,exname)
        b = self.get_all_classid(teacherid)      #获取所有班级i
        json.dumps(b)
        str1 = b
        list1 = json.loads(str1)
        b = self.get_add_class_classId(b,exname)       #获取添加的班级的id
        for i in range(1,10):
            phone = self.phone_num()+str(i)
            name = Unicode(2)
            c = self.add_stu(teacherid,name,"1",phone,b)
            d = self.get_all_stu(b)
            json.dumps(d)
            str2 = d
            list2 = json.loads(str2)
            e = self.get_add_StudentID(d,name)
            stunumber = self.stu_num()+str(i)
            QQnumber = self.QQ_num()+str(i)
            birthdaty = "2018"+"-"+self.birthday()[i-1]
            f = self.edit_add_stu(teacherid,name,"1",phone,stunumber,QQnumber,birthdaty,b,e)





if __name__ == "__main__":
    base_url = "http://192.168.0.167"
    abc = Add_Student(base_url)
    abc.has_stu("18913938700","aa")
#     res = abc.tec_login("18913938700","1")
#     print(res)#登录
#     teacherid = abc.gettecid(res)         #获取登录的教师id
#     print (teacherid)
#     a = abc.add_class(teacherid,u"测试班级")
#     print(a)
#     b = abc.get_all_classid(teacherid)      #获取所有班级id
#     json.dumps(b)
#     print(b)
#     str1 = b
#     list1 = json.loads(str1)
#     print(type(list1))
#     b = abc.get_add_class_classId(b,u"测试班级")       #获取添加的班级的id
#     print(b)
# for i in range(1,10):
#     phone = abc.phone_num()+str(i)
#     print("手机号码是%s"%phone)
#     name = Unicode(2)
#     # name = "好好"
#     c = abc.add_stu(teacherid,name,"1",phone,b)
#     print(c)
#     d = abc.get_all_stu(b)
#     json.dumps(d)
#     print(d)
#     str2 = d
#     list2 = json.loads(str2)
#     print(type(list2))
#     e = abc.get_add_StudentID(d,name)
#     print(e)
#     stunumber = abc.stu_num()+str(i)
#     print("学号是%s"%stunumber)
#     QQnumber = abc.QQ_num()+str(i)
#     birthdaty = "2018"+"-"+abc.birthday()[i-1]
#     f = abc.edit_add_stu(teacherid,name,"1",phone,stunumber,QQnumber,birthdaty,b,e)


