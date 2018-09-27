from random import choice
import random

def TakeOneToList(liststu):#列表分为1个元素和一个不重复元素的子列表
    astu = choice(liststu)
    # print(astu)
    d = [astu]
    c = []
    for i in liststu:
        if (i != astu):
            c.append(i)
    d.append(c)
    return d

def TakeOtherToList(liststu,n):#列表分为一个n个元素的子列表和另外剩下不重复元素的子列表
    astu = random.sample(liststu,n)
    a = []
    a.append(astu)
    c = []
    for i in liststu:
        if (i not in astu):
            c.append(i)
    a.append(c)
    return a

def Take(liststu,stu):#列表根据输入的元素去重后生成新的列表
    a = []
    for i in  liststu:
        if i!=stu:
            a.append(i)
    return a

def TakeStuInGroup(grouplist,stulist):#从学生列表中选择学生加入小组中，保证每一小组中都有学生
   c = []
   if len(stulist)>=len(grouplist):
       for i in range(1,len(grouplist)+1):
           c.append([grouplist[i-1],stulist[i-1]])
       for j in range(len(grouplist)+1,len(stulist)+1):
           c.append([choice(grouplist),stulist[j-1]])
   else:
       print("组数大于学生数！！！")
   print(c)
   return c

def TakeOldtoNewlist(templsit,n):#从旧列表中取值组成新的列表
    a = []
    for i in templsit:
        a.append(str(i[n]))
    return a


if __name__ == '__main__':
    # asd = [0,1,2,3,4,5,6,7,8,9]
    # fgh = TakeOtherToList(asd,8)
    # sad = TakeOneToList(asd)
    # print(fgh)
    # print(type(fgh))
    # print(sad)
    # asd = [0,1,2,3,4,5,6,7,8,9]
    # a = Take(asd,6)
    # print(a)
    a = ["一","二","三"]
    b = [1,2,3,4,5,6,7,8]
    print(TakeStuInGroup(a,b))
    # a = [(1,),(2,),(3,)]
    # print(TakeOldtoNewlist(a,0))