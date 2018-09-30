from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from time import sleep
import os,sys
import requests
import random
import json
import time
import pymssql
import random
from common.Mssql_pub import MssqlUtil
import sys
from random import choice
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

class test():
 def __init__(self,base_url):
        self.url = urljoin(base_url,"kesgo/login.html")
        self.driver=webdriver.Chrome()

 def login(self,txtUsername,txtPassword):
        #大屏端
        self.driver.get(self.url)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)
        self.driver.find_element_by_xpath(".//*[@id='txtUsername']").clear()
        self.driver.find_element_by_xpath(".//*[@id='txtUsername']").send_keys(txtUsername)
        self.driver.find_element_by_xpath(".//*[@id='txtPassword']").clear()
        self.driver.find_element_by_xpath(".//*[@id='txtPassword']").send_keys(txtPassword)
        # sleep(3)
        self.driver.find_element_by_xpath(". //body").click()
        sleep(1)
        self.driver.find_element_by_xpath(".//*[@id='btnLogin']").click()
        sleep(3)
        self.driver.find_element_by_xpath("//*[@id='rtoolbar']/div[1]/a").click()
        sleep(1)
#写思考题并提交432423423423423444444444444444444444444444444444444
 def clickexper(self,i):
        #教师只有一个正在进行中的实验时，这边可以直接点击，多个进行中的这边涉及冒泡了，不能直接用这个
        self.driver.find_element_by_xpath(".//*[@class='m-experiment']/div[2]/ul[1]/li[1]").click()
        #只有第一次才需要
        sleep(3)
        self.driver.find_element_by_xpath(".//*[@id='btnSave']").click()
        sleep(3)
        self.driver.refresh()
        sleep(3)
        #点击思考题进行点评
        self.driver.find_element_by_xpath(".//*[@id='btQuestion']").click()
        list = []
        for ii in range(random.randint(1,i)):#随机点评几次
               a = choice(range(1,i+1))
               b = random.randint(1,5)
               self.driver.find_element_by_xpath("//*[@id='quesPicView']/div/div[1]/div/div/div[{}]/div[2]/div[1]/div/i[{}]".format(a,b)).click()#随机选择某条点评
               list.append({a:b})
               sleep(3)
               # sleep(11)
        # #点击关闭控件关弹出框
        # driver.find_element_by_xpath(".//*[@id='closeFullleft']").click()
        sleep(3)
        #直接点击思考题按钮关闭
        self.driver.find_element_by_xpath(".//*[@id='btQuestion']").click()
        #点击打开视频
        self.driver.find_element_by_xpath(".//*[@id='btVideo']").click()
        #关闭视频
        sleep(3)
        self.driver.find_element_by_xpath(".//*[@id='closeVideo']").click()
        #点击画笔
        # driver.find_element_by_xpath(".//*[@id='icon-editpen']").click()
        sleep(3)
        #点击课堂讨论按钮
        self.driver.find_element_by_xpath(".//*[@id='kttlbtn']").click()
        #提示
        self.driver.find_element_by_xpath(".//*[@class='u-button org']").click()
        sleep(3)
        return list
 def clickgroup(self,n):
        #点击分组按钮
        self.driver.find_element_by_xpath(".//*[@id='fzbtn']").click()
        sleep(3)
        #选择分组
        self.driver.find_element_by_xpath(".//div[@id='g-grounpcont']/div[3]/ul/li[{}]/i".format(n)).click()
        # //*[@id="g-grounpcont"]/div[3]/ul/li[3]/i
        # //*[@id="g-grounpcont"]/div[3]/ul/li[4]/i
        # //*[@id="g-grounpcont"]/div[3]/ul/li[5]/i
        # //*[@id="g-grounpcont"]/div[3]/ul/li[6]/i
        # //*[@id="g-grounpcont"]/div[3]/ul/li[7]/i
        #点击下一步
        self.driver.find_element_by_xpath(".//*[@id='groupnext']").click()
        sleep(3)
        #点击完成分组
        self.driver.find_element_by_xpath(".//*[@id='g-departGrounp']/div[4]/button[2]").click()
        sleep(3)
        #点击开始讨论
        self.driver.find_element_by_xpath(".//*[@id='g-someonenogroup']/div[3]/button").click()
        sleep(3)
 def clickgroup1(self):
        #点击分组按钮
        self.driver.find_element_by_xpath(".//*[@id='fzbtn']").click()
        sleep(3)
        #选择观点分组
        self.driver.find_element_by_xpath(".//div[@id='g-grounpcont']/div[3]/ul/li[1]/i").click()
        #点击下一步
        self.driver.find_element_by_xpath(".//*[@id='groupnext']").click()
        sleep(3)
        #学生加入分组#学生加入分组#学生加入分组#学生加入分组#学生加入分组#学生加入分组
 def clickgroup2(self):
        #点击完成分组
        self.driver.find_element_by_xpath(".//*[@id='g-departGrounp']/div[4]/button[2]").click()
        sleep(3)
        #点击确定
        self.driver.find_element_by_xpath("//*[@id='poptips']/div[3]/button[2]").click()
        sleep(3)
        #点击开始讨论
        self.driver.find_element_by_xpath(".//*[@id='g-someonenogroup']/div[3]/button").click()
        sleep(3)
        # #点击讨论的放大按钮
        # driver.find_element_by_xpath(".//*[@id='leftFullScreen']").click()
        # #点击讨论问题
        # driver.find_element_by_xpath(".//*[@id='g-someonenogroup']/div[3]/button").click()

#分组后发送观点讨论的组长发言432222222222222222222222222222222222222222222222
#self.driver.refresh()
#sleep(3)

#观点讨论我的互动432423423423423423423423423423423423423423442342342
#self.driver.refresh()
#sleep(3)

 def speakComment(self,i):
        #点击发言点评
        self.driver.find_element_by_xpath(".//*[@id='diagnosisGrade']").click()
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='gradeSubmit']").click()
        sleep(3)
        # #对发言进行点评
        list = []
        for ii in range(random.randint(1,i)):#随机点评几次
               a = choice(range(1,i+1))
               b = random.randint(1,5)
               self.driver.find_element_by_xpath(".//*[@id='drawCoverDiv']/div[{}]/div[2]/i[{}]".format(a,b)).click()#随机选择某条点评
               list.append({a:b})
               sleep(3)
               # sleep(11)
        #点击开始提问
        self.driver.find_element_by_xpath(".//*[@id='diagnosisGrade']").click()
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='gradeSubmit']").click()
        sleep(3)
        return list
        #关闭弹出框(3秒会自动消失)
        # driver.find_element_by_xpath(".//*[@id='g-boyitip/]/div/i").click()

#组间博弈提问A→B423423423423423423423423423423423423423432423423423432
#self.driver.refresh()
#sleep(3)

#组间博弈提问B→Afdgfdddddddddddddddddddddddddddddddddddddddddddddddg
#self.driver.refresh()
#sleep(3)

 def questionComment1(self):#n是提问的组数
        #点击点评按钮
        self.driver.find_element_by_xpath(".//*[@id='btnaskcommon']").click()
        #提示点击确定
        sleep(3)
        self.driver.find_element_by_xpath(".//*[@id='confirmCommontip']").click()
 def questionComment2(self,i,j):
        # #对提问进行点评
        k = random.randint(1,5)
        self.driver.find_element_by_xpath((".//*[@id='drawCoverDiv']/div[{}]/div[{}]/i[{}]").format(i,j,k)).click()
        sleep(3)
        # sleep(11)
        return k
 def questionComment3(self):
        #点击回答按钮
        self.driver.find_element_by_xpath(".//*[@id='btnanswer']").click()
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='confirmBeginAskTip']").click()
        sleep(3)

#组间博弈回答A回答423423423432432423423432432423432423
#self.driver.refresh()
#sleep(3)

#组间博弈回答B回答32131321321312312312312312312
#self.driver.refresh()
#sleep(3)

 def answerComment1(self):
        #点击回答点评
        self.driver.find_element_by_xpath(".//*[@id='btnaskcommon']").click()
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='confirmCommontip']").click()
 def answerComment2(self,i,j):
        # #对回答进行点评
        k = random.randint(1,5)
        self.driver.find_element_by_xpath((".//*[@id='drawCoverDiv']/div[{}]/div[{}]/i[{}]").format(i,j,k)).click()
        sleep(3)
        # sleep(11)
        return k
 def answerComment3(self):
        #点击开始诊断
        self.driver.find_element_by_xpath(".//*[@id='btnanswer']").click()
        #提示点击确定
        self.driver.find_element_by_xpath(".//*[@id='confirmBeginAskTip']").click()
        #点击知道了
        self.driver.find_element_by_xpath(".//*[@id='knowdiagnosise']").click()
        sleep(3)

#诊断总结组长发言44324233333333333333333234234234234234234234234234234242
#self.driver.refresh()
#sleep(3)

#诊断总结我的互动43243243243243243242343242342342342342342342
#self.driver.refresh()
#关闭我知道了弹出框
#self.driver.find_element_by_xpath(".//*[@id='knowdiagnosise']").click()
#sleep(3)

 def diagnosisComment(self,i):
        #点击诊断点评按钮
        self.driver.find_element_by_xpath(".//*[@id='diagnosisGrade']").click()
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='gradeSubmit']").click()
        sleep(3)
        list = []
        # #对诊断进行点评
        for ii in range(random.randint(1,i)):#随机点评几次
               a = choice(range(1,i+1))
               b = random.randint(1,5)
               self.driver.find_element_by_xpath(".//*[@id='drawCoverDiv']/div[{}]/div[2]/i[{}]".format(a,b)).click()#随机选择某条点评
               list.append({a:b})
               sleep(3)
               # sleep(11)
        #提示课堂成绩
        self.driver.find_element_by_xpath(".//*[@id='courseScore']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='scoreSubmit']").click()
        sleep(3)
        return list

#小组投票54354354353454354353453453454353453453534534543
#self.driver.refresh()
#sleep(3)

 def endgroupVote(self,i):
        #结束投票
        self.driver.find_element_by_xpath(".//*[@id='overVote']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(3)
        list = []
        for ii in range(random.randint(1,i)):
               # 获取滑动条的size
               anumber = choice(range(1,i+1))
               span_background = self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/div/input".format(anumber))
               span_background_size = span_background.size
               a = (span_background_size["width"]/100)
               # 获取滑块的位置
               button = span_background
               button_location = button.location
               # 拖动操作：drag_and_drop_by_offset
               # 将滑块的位置由初始位置，右移一个滑动条长度（即为x坐标在滑块位置基础上，加上滑动条的长度，y坐标保持滑块的坐标位置）
               n = random.randint(-63,37)
               x_location = button_location["x"]+n*a
               y_location = button_location["y"]
               ActionChains(self.driver).drag_and_drop_by_offset(button, x_location, y_location).perform()
               # self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/p/span[contains(text(),'48')]".format(choice(range(1,i+1)))).click()
               # self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/div/input".format(choice(range(1,i+1)))).send_keys("33")
               sleep(2)
               asd = self.driver.find_element_by_xpath("./html/body/form/div[2]/div[2]/div[2]/div/div[{}]/p/span".format(anumber)).text
               # print("n是%s"%n,"63+n是%s"%(63+n),"asd是%s"%asd)
               sleep(5)
               list.append({anumber:int(asd)})
        #点击结束评分
        self.driver.find_element_by_xpath(".//*[@id='overGrade']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(10)
        #点击个人表现
        self.driver.find_element_by_xpath(".//*[@class='m-tabnavi']/a[2]").click()
        sleep(3)
        return list
#个人投票321321321321321321321321321321312321
#self.driver.refresh()
#A.mssql_close()
#sleep(3)

 def endpersonalVote(self):
        #点击结束投票
        self.driver.find_element_by_xpath(".//*[@id='overVote']").click()
        sleep(3)
        #提示点击确定按钮
        self.driver.find_element_by_xpath(".//*[@id='btnSubmit']").click()
        sleep(3)
        #关闭mvp按钮
        self.driver.find_element_by_xpath(".//*[@id='closemvp']").click()
        sleep(3)
        #点击成绩统计
        self.driver.find_element_by_xpath(".//*[@class='m-tabnavi']/a[3]").click()
        sleep(3)
        #点击左边退出按钮
        self.driver.find_element_by_xpath(".//*[@id='u-infol']/span/i").click()
        sleep(10)
        #退出课程
        self.driver.find_element_by_xpath("//*[@id='m-InfoBar']/div[2]/a[1]").click()
        sleep(3)
        #点击左边退出按钮
        self.driver.find_element_by_xpath(".//*[@id='u-infol']/span/i").click()
        sleep(10)
        #退出登录
        self.driver.find_element_by_xpath("//*[@id='m-InfoBar']/div[2]/a").click()



if __name__ == "__main__":
   test('12345678922','1','rett453')
