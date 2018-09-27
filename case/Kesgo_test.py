import requests
from case.Kesgo_ifcode import ScreenOperationOne,ScreenOperationTwo,ScreenOperationTmp
from case.Kesgo_screen import test
from time import  sleep
import random
from common.Take_OtherToList import *
from tomorrow import threads
import threading
from common.writeexcel import *
from common.readexcel import *
import xlrd
from common.Calculation_score import *
from common.logger import *

# if __name__ == "__main__":
def wexcel(base_url,mb,exname):
    #实验需要有至少两道思考题（一道问答一道选择）、有视频，需要多个学生能完成分组，每组都有学生
    s = requests.session()
    ListCountSum = []
#基础设置
    uioper = test(base_url)
    interoperone = ScreenOperationOne(s,base_url,mb,exname)
    numb = random.randint(1,5)
    stulen = interoperone.StuLen#班级学生总数
    i = random.randint(1,stulen)#随机取数i
    stulisti = interoperone.Random_StuSel(i)#随机取i个学生的列表
    stulistsum = interoperone.StuList#学生总数的列表
    ExperimentID = interoperone.ExperimentID1#实验id
    wt = Write_excel("C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx")
    log = Log()
#进入实验提交思考题
    listcount1 = []#记录提交思考题的学生id，按时间顺序排列
    uioper.login(mb,"1")#大屏登录
    for stui in stulisti:#从随机生成的学生列表里取学生提交思考题
        interoperone.WriteQuestion(str(stui[0]))#手机写思考题、获取写的内容、提交思考题
        listcount1.append(str(stui[0]))
#分组
    listcount11 = uioper.clickexper(i)#大屏点击进入实验并点评思考题然后点击分组、开始讨论，记录评了第几条思考题以及评星数
    log.info("---测试开始----")
    log.info("提交思考题的学生id列表,按时间顺序排列：%s"%listcount1+","+"评第几个思考题评多少星列表：%s"%listcount11)
    # print("提交思考题的学生id列表,按时间顺序排列：%s"%listcount1,"评第几个思考题评多少星列表：%s"%listcount11)
    setgroupno = choice(range(1,8))#随机选择分组方式
    # setgroupno = 1
    if setgroupno == 1:
        uioper.clickgroup1()
        screenOperationtmp = ScreenOperationTmp(ExperimentID)
        trueGroupidlist = TakeOldtoNewlist(screenOperationtmp.Groupidlist,0)#小组列表
        trueStuidlist = TakeOldtoNewlist(stulistsum,0)#学生列表
        postlist = TakeStuInGroup(trueGroupidlist,trueStuidlist)#学生和小组的列表
        for post in postlist:
            screenOperationtmp.JoinGroup(post[0],post[1])#加组
        uioper.clickgroup2()
    else:uioper.clickgroup(setgroupno)
#基础设置
    interopertwo = ScreenOperationTwo(s,base_url,mb,exname)
    groupstulen = interopertwo.GroupStuLen#小组数量
    k = random.randint(1,groupstulen)#随机取数k
    groupstulistk = interopertwo.Random_GroupStuSel(k)#随机取K个组长的列表
    groupstulistsum = interopertwo.GroupStuList#组长总数的列表
    Speechcountlist1 = []
    Speechcountlist2 = []
#开始观点讨论
    listcount2 = []#记录发言的小组id，组长id、小组orderno
    def aaa():
      for groupstuk in groupstulistk:
          for i in range(random.randint(1,4)):
             interopertwo.TLGruopleaderSpeak(str(groupstuk[0]),str(groupstuk[1]),str(groupstuk[2]),str(groupstuk[3])) #观点讨论组长发言
             listcount2.append((str(groupstuk[0]),str(groupstuk[1]),str(groupstuk[2])))
             Speechcountlist1.append(str(groupstuk[1]))
             uioper.driver.refresh()
             sleep(3)
    # print("组长数是%s"%k)
    listcount22 = []#记录互动的学生id
    def bbb():
      ii = random.randint(1,stulen)#随机取数ii
      stulistii = interoperone.Random_StuSel(ii)#随机取ii个学生
      for stuii in stulistii:
         for i in range(random.randint(1,4)):
             interopertwo.TLInteractionSpeak(str(stuii[0]))#观点讨论我的互动
             Speechcountlist2.append(str(stuii[0]))
             listcount22.append(str(stuii[0]))
             # uioper.driver.refresh()
             sleep(3)
    # @threads(2)
    # def run_test(function):
    #     return function()
    #
    # numbers = [aaa,bbb]
    # for i in numbers:
    #     run_test(i)
    # sleep(100)
    funcs = [aaa,bbb]
    athreads = []
    for func in funcs:
          thread = threading.Thread(target=func)
          athreads.append(thread)
    for thread in athreads:
          thread.start()
    for thread in athreads:
          thread.join()
    sleep(0.1)
#开始提问
    sleep(3)
    listcount222 = uioper.speakComment(k)#发言点评并点击开始提问
    log.info("发言的小组id、组长id、小组orderno列表：%s"%listcount2+","+"互动的学生id列表：%s"%listcount22+","+"评第几个发言评多少星列表%s"%listcount222)
    # print("发言的小组id、组长id、小组orderno列表：%s"%listcount2,"互动的学生id列表：%s"%listcount22,"评第几个发言评多少星列表%s"%listcount222)
    temlist = []
    listcount3 = []#提问小组id、组长id、小组orderno列表
    for i in range(random.randint(1,10)):#随机提问几次
        ask = TakeOneToList(groupstulistsum)
        ask1 = ask[0]
        ask1stuid = str(ask1[1])#随机选择一个组长去提问
        ask2 = ask[1]
        ask2sel = choice(ask2)#随机选择一个组长被提问
        AskQuestionID = interopertwo.AaskB(str(ask1[0]),str(ask1[3]),str(ask2sel[0]),str(ask2sel[3]),str(ask1[1]),str(ask1[2]))#提问
        temlist.append([AskQuestionID,ask1,ask2sel])#存放所有的提问数据
        Speechcountlist1.append(str(ask1[1]))
        listcount3.append((str(ask1[0]),str(ask1[1]),str(ask1[2])))
        uioper.driver.refresh()
        sleep(3)
    # print(temlist)
    asklen = len(temlist)
    log.info("提问小组id、组长id、小组orderno列表%s"%listcount3)
    # print("提问小组id、组长id、小组orderno列表%s"%listcount3)
#点击提问点评
    uioper.questionComment1()
    ordernolist = []
    for temi in temlist:
        if str(temi[1][2]) not in ordernolist:
            ordernolist.append(str(temi[1][2]))#不重复取出所有的提问组的orderno eg[6,1,3,4]
    # print("我是ordernoliat：%s"%ordernolist)
    ordernolist.sort()#升序排序 eg[1,3,4,6]
    # print("我是升序后的ordernoliat：%s"%ordernolist)
    orderlen = len(ordernolist)#多少个组提问 eg 4个组
    # for i in range(random.randint(1,orderlen)):#随机点评几次
    listcount33 = []
    for i in range(random.randint(1,15)):#随机点评几次
        ranordernoNum = choice(range(1,orderlen+1))#随机取第几个orderno  eg随机取[1,3,4,6]中的第4个
        ranorderno = ordernolist[ranordernoNum-1]#随机取的orderno   eg随机取的6
        n = 0#该组提问总数
        nasked = []#被提问组列表
        for j in temlist:
            if str(j[1][2]) == ranorderno:
                nasked.append(str(j[2][2]))
                n = n+1
        set1 = set(nasked)#可以对一个小组提问多次，去重
        nset1 = len(set1)
        askconstar = uioper.questionComment2(ranordernoNum+1,nset1+1)#提问点评
        listcount33.append({ranordernoNum:askconstar})
    log.info("评第几个提问评多少星列表%s"%listcount33)
    # print("评第几个提问评多少星列表%s"%listcount33)
    uioper.questionComment3()
    # j = random.randint(1,groupstulen-1)#随机取数j
    # GrouplistPart = TakeOtherToList(groupstulistsum,j)#将组长列表随机分成两部分
    # AGrouplistPart = GrouplistPart[0]#准备提问的组长列表
    # BGrouplistPart = GrouplistPart[1]#准备接受提问的组长列表
    # print(len(AGrouplistPart))
    # print(len(BGrouplistPart))
    # print(numb)
    # temlist = []
    # for groupstup in AGrouplistPart:#提问
    #     for togroupstup in BGrouplistPart:
    #         for ii in range(numb):
    #             AskQuestionID = interopertwo.AaskB(str(groupstup[0]),str(groupstup[3]),str(togroupstup[0]),str(togroupstup[3]),str(groupstup[1]),str(groupstup[2]))
    #             temlist.append([AskQuestionID,togroupstup])
    #             uioper.driver.refresh()
    #             sleep(3)

#开始回答
    listcount4 = []#回答小组id、组长id、小组orderno列表
    answerlist = []
    for answerno in  range(random.randint(1,asklen)):#随机回答几次
        answer = choice(temlist)#随机挑一个回答
        interopertwo.Aanswer(answer[0],str(answer[2][1]),str(answer[2][0]),str(answer[2][3]),str(answer[2][2]))
        answerlist.append(answer)#记录回答的数据
        Speechcountlist1.append(str(answer[2][1]))
        listcount4.append((str(answer[2][0]),str(answer[2][1]),str(answer[2][2])))
        uioper.driver.refresh()
        sleep(3)
    log.info("回答小组id、组长id、小组orderno列表%s"%listcount4)
    # print("回答小组id、组长id、小组orderno列表%s"%listcount4)
    # print(answerlist)
#回答点评
    uioper.answerComment1()
    answerordernolist = []
    for answertemi in answerlist:
        if str(answertemi[2][2]) not in answerordernolist:
            answerordernolist.append(str(answertemi[2][2]))#不重复取出所有的回答组的orderno eg[6,1,3,4]
    # print("我是answerordernolist：%s"%answerordernolist)/
    answerordernolist.sort()#升序排序 eg[1,3,4,6]
    # print("我是升序后的answerordernolist：%s"%answerordernolist)
    answerorderlen = len(answerordernolist)#多少个组回答 eg 4个组
    listcount44 = []
    for i in range(random.randint(1,answerorderlen)):#随机点评几次
        rananswerordernoNum = choice(range(1,answerorderlen+1))#随机取第几个orderno  eg随机取[1,3,4,6]中的第4个
        rananswerorderno = answerordernolist[rananswerordernoNum-1]#随机取的orderno   eg随机取的6
        nn = 0#该组回答总数
        que = []#该组回答的问题列表
        # nask = []#该组回答的提问组列表
        for j in answerlist:
            if str(j[2][2]) == rananswerorderno:
                nn = nn+1
                que.append(j[0])
                # nask.append(str(j[1][2]))
        set3 = set(que)
        nset3 = len(set3)
        # set2 = set(nask)
        # nset2 = len(set2)
        answerconstar = uioper.answerComment2(rananswerordernoNum+1,nset3+1)#回答点评
        listcount44.append({rananswerordernoNum:answerconstar})
    log.info("评第几个回答评多少星列表%s"%listcount44)
    # print("评第几个回答评多少星列表%s"%listcount44)
    uioper.answerComment3()
#诊断总结
    kk = random.randint(1,groupstulen)#随机取数kk
    groupstulistkk = interopertwo.Random_GroupStuSel(kk)#随机取KK个组长
    listcount5 = []#记录诊断的小组id，组长id、小组orderno
    def ccc():
     for groupstukk in groupstulistkk:
         interopertwo.ZDGruopleaderSpeak(str(groupstukk[0]),str(groupstukk[2]),str(groupstukk[3]),str(groupstukk[1]))#诊断总结组长发言
         listcount5.append((str(groupstukk[0]),str(groupstukk[1]),str(groupstukk[2])))
         Speechcountlist1.append(str(groupstukk[1]))
         uioper.driver.refresh()
         sleep(3)
    alen = interopertwo.Alen#学生数
    alist = interopertwo.Alist#学生列表
    iii = random.randint(1,alen)#随机取数iii
    stulistiii = interopertwo.Random_ASel(iii)#随机取iii个学生
    listcount55 = []
    def ddd():
     for stu in stulistiii:
         interopertwo.ZDInteractionSpeak(str(stu[0]),str(stu[2]),str(stu[3]),str(stu[1]))#诊断总结我的互动
         listcount55.append((str(stu[0]),str(stu[1]),str(stu[2])))
         Speechcountlist2.append(str(stu[1]))
         # uioper.driver.refresh()
         sleep(3)
    funcs2 = [ccc,ddd]
    athreads2 = []
    for func2 in funcs2:
          thread2 = threading.Thread(target=func2)
          athreads2.append(thread2)
    for thread2 in athreads2:
          thread2.start()
    for thread2 in athreads2:
          thread2.join()
    sleep(0.1)
    uioper.driver.find_element_by_xpath(".//*[@id='knowdiagnosise']").click()#关闭我知道了弹出框
    listcount555 = uioper.diagnosisComment(kk)#点击诊断点评后点击课堂成绩
    log.info("诊断的小组id、组长id、小组orderno列表：%s"%listcount5+","+"互动的小组id、学生id、小组orderno列表：%s"%listcount55+","+"评第几个诊断评多少星列表%s"%listcount555)
    # print("诊断的小组id、组长id、小组orderno列表：%s"%listcount5,"互动的小组id、学生id、小组orderno列表：%s"%listcount55,"评第几个诊断评多少星列表%s"%listcount555)
#小组投票
    groupidlist = []#初始记录列表
    grouplist = []
    for groupstu in groupstulistsum:
        groupidlist.append(str(groupstu[0]))#取出所有groupid
        grouplist.append((str(groupstu[0]),str(groupstu[1]),str(groupstu[2])))#取出所有的小组id，组长id，order no
    algrovoted = []
    listcount6 = []#记录被投小组id
    for groupvotenum in  range(random.randint(1,10)):
        b = choice(alist)
        bpart1stuid = str(b[1])#随机选择一个学生去投票
        bpart1groupid = str(b[0])#所选学生所在小组
        if bpart1stuid not in algrovoted:
            Remainlist = Take(groupidlist,bpart1groupid)#获取除去当前所选学生所在的小组的小组列表
            toGroupID = choice(Remainlist)#选择一个小组被投票
            interopertwo.Groupvote(bpart1stuid,toGroupID)#小组投票
            listcount6.append(toGroupID)
            uioper.driver.refresh()
            sleep(3)
            algrovoted.append(bpart1stuid)
    listcount66 = uioper.endgroupVote(kk)#结束投票
    log.info("被投票小组id列表%s"%listcount6+","+"评第几个小组评多少分列表%s"%listcount66)
    # print("被投票小组id列表%s"%listcount6,"评第几个小组评多少分列表%s"%listcount66)
#个人投票
    alpervoted = []#初始记录列表
    listcount7 = []#被投票学生列表
    for personalvotenum in range(random.randint(1,10)):
        a = TakeOneToList(alist)
        apart1 = a[0]
        apart1stuid = str(apart1[1])#随机选择一个学生去投票
        if apart1stuid not in alpervoted:
            apart2 = a[1]
            apart2stuid = str(choice(apart2)[1])#随机选择一个学生被投票
            interopertwo.Personalvote(apart1stuid,apart2stuid)#投票
            listcount7.append(apart2stuid)
            uioper.driver.refresh()
            sleep(3)
            alpervoted.append(apart1stuid)#投过票的加入记录列表里
    log.info("被投票学生id列表%s"%listcount7)
    # print("被投票学生id列表%s"%listcount7)
    interopertwo.Closeconn()
    uioper.endpersonalVote()#结束投票并退出等
    uioper.driver.quit()
    # print("a=%s"%alen)
    # print("b=%s"%stulen)

#写入标题
    score = Score()
    coln = 1
    colnames=["学生id","思考题得分","思考题评分","发言得分","发言评分",
              "提问、回答得分","提问、回答评分","诊断得分","诊断评分","小组投票得分","小组教师评分","个人投票得分","个人发言得分","课堂讨论","小组表现","个人表现","总分"]
    for colname in colnames:
        wt.writee(1,coln ,colname)
        coln+=1
    rown = 2#将学生id写进excel第一列，第二行开始
    for stuid in stulistsum:
        wt.writee(rown, 1,str(stuid[0]))
        rown+=1
    excel = Excelread("C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx","Sheet")
    table = excel.table
    rowNum = excel.rowNum    # 获取总行数
    colNum = excel.colNum    # 获取总列数
    scored = score.getscore(listcount1,listcount11)#获取学生思考题实际评分
    log.info("学生思考题评分%s"%scored)
    # print(scored)
#写入思考题得分和思考题评分
    for i in range(1,rowNum):#循环取每一行的学生数据
        values = table.row_values(i)
        #将取到的学生id是否在提交思考题的学生id里
        if str(values[0]) in listcount1:
            wt.writee(i+1, 2,5)
            if str(values[0]) in scored.keys():#该学生是否被评分，评了多少星
                wt.writee(i+1, 3,scored[str(values[0])]*5/5)
            else:
                wt.writee(i+1, 3,0)
        else:
            wt.writee(i+1, 2,0)
            wt.writee(i+1, 3,0)
    listsum = []
#计算发言得分
    speakscorelist = score.getsysscore(listcount2,15)
    log.info("学生发言得分%s"%speakscorelist)
    # print("学生发言得分%s"%speakscorelist)
    listsum.append(speakscorelist)
#计算发言评分
    speakscoredlist = score.gettecscored(listcount2,listcount222,5/5)
    log.info("学生发言评分%s"%speakscoredlist)
    # print("学生发言评分%s"%speakscoredlist)
    listsum.append(speakscoredlist)
#计算提问回答得分
    askandanswerscorelist = score.getsysscore(listcount3+listcount4,15)
    log.info("学生提问、回答得分%s"%askandanswerscorelist)
    # print("学生提问、回答得分%s"%askandanswerscorelist)
    listsum.append(askandanswerscorelist)
#计算提问评分
    askscoredlist = score.gettecscored(listcount3,listcount33,5/5)
    log.info("学生提问评分%s"%askscoredlist)
    # print("学生提问评分%s"%askscoredlist)
#计算回答评分
    answerscoredlist = score.gettecscored(listcount4,listcount44,5/5)
    log.info("学生回答评分%s"%answerscoredlist)
    # print("学生回答评分%s"%answerscoredlist)
    aask = askscoredlist
    banswer = answerscoredlist
    for bkey,bvalue in banswer.items():
        if bkey not in aask.keys():
            aask[bkey]=bvalue
        elif bkey in aask.keys():
             if bvalue ==0:
                  aask[bkey]=aask[bkey]
             elif aask[bkey] ==0:
                  aask[bkey]=bvalue
             else:
                  aask[bkey]=(aask[bkey]+bvalue)/2
    # print(aask)
    log.info("学生提问、回答评分%s"%aask)
    # print("学生提问、回答评分%s"%aask)
    listsum.append(aask)
#计算诊断得分
    Diagscorelist = score.getsysscore(listcount5,15)
    log.info("学生诊断得分%s"%Diagscorelist)
    # print("学生诊断得分%s"%Diagscorelist)
    listsum.append(Diagscorelist)
#计算诊断评分
    Diagscoredlist = score.gettecscored(listcount5,listcount555,5/5)
    log.info("学生诊断评分%s"%Diagscoredlist)
    # print("学生诊断评分%s"%Diagscoredlist)
    listsum.append(Diagscoredlist)
#计算小组表现-小组投票得分
    Groupvotscorelist = score.getsysscore(listcount6,10)
    log.info("学生小组投票得分%s"%Groupvotscorelist)
    # print("学生小组投票得分%s"%Groupvotscorelist)
    listsum.append(Groupvotscorelist)
#计算小组表现-小组教师评分
    GroupTecscoredlist = score.gettecscored2(grouplist,listcount66,5/100)
    log.info("学生小组教师评分%s"%GroupTecscoredlist)
    # print("学生小组教师评分%s"%GroupTecscoredlist)
    listsum.append(GroupTecscoredlist)
#计算个人表现-个人投票得分
    Personvotscorelist = score.getsysscore2(listcount7,5)
    log.info("学生个人投票得分%s"%Personvotscorelist)
    # print("学生个人投票得分%s"%Personvotscorelist)
    listsum.append(Personvotscorelist)
#计算个人表现-个人发言得分
    Speechcountlist = Speechcountlist1+Speechcountlist2
    Speechcountscorelist = score.getsysscore2(Speechcountlist,5)
    log.info("学生个人发言得分%s"%Speechcountscorelist)
    # print("学生个人发言得分%s"%Speechcountscorelist)
    listsum.append(Speechcountscorelist)
#写入剩余分数
    col = 4
    for list in listsum:
        for i in range(1,rowNum):
            values = table.row_values(i)
            if str(values[0]) in list.keys():
                wt.writee(i+1, col,list[str(values[0])])
            else:
                wt.writee(i+1, col,0)
        col+=1
#读取excel
    excel1 = Excelread("C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx","Sheet")
    rr = excel1.dict_data()
    # print("excel中值列表为：%s"%rr)
    log.info("excel中值列表为：%s"%rr)
    for r in rr:
        Classdiscuss = (r["发言得分"])+(r["发言评分"])+(r["提问、回答得分"])+(r["提问、回答评分"])+(r["诊断得分"])+(r["诊断评分"])
        Groupperfor = (r["小组投票得分"])+(r["小组教师评分"])
        Personalperfor = (r["个人投票得分"])+(r["个人发言得分"])
        Totalscore = (r["思考题得分"])+(r["思考题评分"])+(r["发言得分"])+(r["发言评分"])+(r["提问、回答得分"])+(r["提问、回答评分"])+\
                     (r["诊断得分"])+(r["诊断评分"])+(r["小组投票得分"])+(r["小组教师评分"])+(r["个人投票得分"])+(r["个人发言得分"])
        wt.writee((r["rowNum"]), 14,Classdiscuss)
        wt.writee((r["rowNum"]), 15,Groupperfor)
        wt.writee((r["rowNum"]), 16,Personalperfor)
        wt.writee((r["rowNum"]), 17,Totalscore)
    log.info("----测试结束----")



if __name__ == '__main__':
    base_url = "http://192.168.0.167"
    mb = "18913938700"
    exname = "cccttt"
    wexcel(base_url,mb,exname)





