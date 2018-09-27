import random
from time import  sleep

import requests

from case.Kesgo_screen import test
from case.old_code.FZhcode_old import ScreenOperationOne,ScreenOperationTwo

if __name__ == "__main__":
    #实验需要有至少两道思考题（一道问答一道选择）、有视频，需要多个学生能随机分组
    base_url = "http://192.168.0.167"
    s = requests.session()
    mb = "18913938700"
    exname = "zxc"
    uioper = test(base_url)
    #uioper.login(mb,"1")#大屏登录
    interoperone = ScreenOperationOne(s,base_url,mb,exname)

    uioper.login(mb,"1")#大屏登录
    interoperone.WriteQuestion()#手机写思考题
    d = interoperone.GetPreviewID() #获取写的内容
    interoperone.SubmitQuestion(d)#提交思考题

    uioper.clickexper()#大屏点击进入实验并点评思考题然后点击分组、开始讨论
    interopertwo = ScreenOperationTwo(s,base_url,mb,exname)
    for i in range(random.randint(1,20)):
        interopertwo.TLGruopleaderSpeak() #观点讨论组长发言
        uioper.driver.refresh()
        sleep(3)
    for i in range(random.randint(1,20)):
        interopertwo.TLInteractionSpeak()#观点讨论我的互动
        uioper.driver.refresh()
        sleep(3)
    uioper.speakComment()#发言点评并点击开始提问
    AskQuestionIDA_B = interopertwo.AaskB() #A向B提问
    uioper.driver.refresh()
    sleep(3)
    AskQuestionIDB_A = interopertwo.BaskA()#B向A提问
    uioper.driver.refresh()
    sleep(3)
    uioper.questionComment()#提问点评并点击开始回答
    interopertwo.Aanswer(AskQuestionIDB_A)#A回答
    uioper.driver.refresh()
    sleep(3)
    interopertwo.Banswer(AskQuestionIDA_B)#B回答
    uioper.driver.refresh()
    sleep(3)
    uioper.answerComment()#回答点评
    for i in range(random.randint(1,20)):
        interopertwo.ZDGruopleaderSpeak()#诊断总结组长发言
        uioper.driver.refresh()
        sleep(3)
    for i in range(random.randint(1,20)):
        interopertwo.ZDInteractionSpeak()#诊断总结我的互动
        uioper.driver.refresh()
        sleep(3)
    uioper.driver.find_element_by_xpath(".//*[@id='knowdiagnosise']").click()#关闭我知道了弹出框
    sleep(3)
    uioper.diagnosisComment()#点击诊断点评后点击课堂成绩
    interopertwo.Groupvote()#小组投票
    uioper.driver.refresh()
    sleep(3)
    uioper.endgroupVote()#结束投票
    interopertwo.Personalvote()#个人投票
    interopertwo.Closeconn()
    uioper.driver.refresh()
    sleep(3)
    uioper.endpersonalVote()#结束投票并退出等
    uioper.driver.quit()







