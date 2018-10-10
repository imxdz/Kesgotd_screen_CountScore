#-*- coding:utf-8 -*-
from case.Kesgo_Backstage.kesgo_screen_para import *
from selenium import webdriver
from time import sleep
from common.Generate_Random import *
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin
from case.Kesgo_addstudent import *

def backstage(base_url,tecphonenum,exname):
 login = Login()
 teachLogin = TeachLogin()
 adminurl = urljoin(base_url,"kesgo/admin/login.html")
 tecurl = urljoin(base_url,"kesgo/login.html")

 driver=webdriver.Chrome()
 # 后台管理员端
 driver.get(adminurl)
 driver.maximize_window()
 driver.implicitly_wait(10)
 # 登录
 login.user_login(driver,"apadmin","654321")
 # 课程管理-教师管理
 login.user_teachermanager(driver,Unicode(3),tecphonenum,"11@qq.com","test111","111111")
 # #退出登录
 login.user_logout(driver)

 #教师端
 driver.get(tecurl)
 driver.maximize_window()
 driver.implicitly_wait(10)
 #教师登录
 teachLogin.user_login(driver,tecphonenum,"1")
 # 诊断工具
 login.user_toolmanage(driver,Unicode(3),Unicode(3),3,Unicode(3))
 # 课程管理-新建课程
 login.user_addcourse(driver,Unicode(3))
 # 定位课程位置
 login.user_coursecur(driver)
 # 课程管理-章节管理
 login.user_chaptermanagement(driver,Unicode(3),1,Unicode(3))
 # 课程管理-微课管理
 login.user_microclassmanagement(driver,Unicode(3))
 # 课程管理-案例管理
 login.user_casemanagement(driver,Unicode(3),Unicode(3),Unicode(3),1,Unicode(3),1,Unicode(3),Unicode(3),Unicode(3),Unicode(3),Unicode(3),Unicode(3))
 # 添加班级学生
 Add_Student(base_url).has_stu(tecphonenum,exname)
 # teachLogin.user_classmanage(driver,Unicode(3))
 # 添加实验
 teachLogin.user_experimentmanager(driver,exname)
 # 退出登录
 teachLogin.user_logout(driver)
 # 关闭浏览器
 driver.quit()

if __name__ == '__main__':
      tecphonenum = tecphone_num()
      exname = Unicode(3)
      base_url = "http://192.168.0.167"
      backstage(base_url,tecphonenum,exname)