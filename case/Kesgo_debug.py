from random import choice
import random
# def TakeOtherStuToList(liststu):
#     astu = choice(liststu)
#     print(astu)
#     c = []
#     for i in liststu:
#         if (i != astu):
#             c.append(i)
#     return c
#
#
#
# if __name__ == '__main__':
#     asd = [0,1,2,3,4,5,6,7,8,9]
#     fgh = TakeOtherStuToList(asd)
#     print(fgh)
#     print(type(fgh))

# import  random
# list = [0,1,2,3,4,5]
# print()
# print(type(len(list)))
#
#
# list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# slice = random.sample(list, 5)  #从list中随机获取5个元素，作为一个片断返回
# print (slice)
# print (list) #原有序列并没有改变。
#
#
# listaa = ["1","2","3"]
# for i in listaa:
#     print(i)
#     print(type(i))
class a():
    def __init__(self):
        self.a = 1
        self.b = 2
    def add(self):
        aa = self.a+self.b
        return aa
class b(a):
    def __init__(self):
        super(b,self).__init__()
        self.aa = 3
        self.bb = 4
import requests
def TNSubmitBrainDiagnosis():
    #诊断总结
    TNSubmitBrainDiagnosis_url = "http://192.168.0.167/kesgo.Service/wcf/DiagnoseService.svc/SubmitBrainDiagnosis"
    TNSubmitBrainDiagnosis_body = {"braindiagno":"{\"GroupID\":\"1070AEB9-35A6-4EBE-BB11-67D3636F9C99\",\"ContentImg\":\"\",\"SpeakContent\":\"td\",\"ExperimentID\":\"3C8E265B-D9A8-45F5-9247-BD33537190D4\",\"Title\":\"td\"}"}
    h5 = {
      "Accept": "application/json, text/plain, */*",
      "User-Agent": "Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/58.0.3029.83 Mobile Safari/537.36",
      "Content-Type": "application/json;charset=UTF-8"
     }
    TNSubmitBrainDiagnosis_r = requests.post(TNSubmitBrainDiagnosis_url, json=TNSubmitBrainDiagnosis_body,headers=h5)
    print(TNSubmitBrainDiagnosis_r.text)
if __name__ == '__main__':
    # a = [1,2,3,3,4,5,5,5,6]
    # print(a)
    # set1=set(a)
    # print(set1)
    # print(len(set1)) #len(set1)即为列表中不同元素的数量
    l =[1, 2, [3, [4, 5, 6, [7, 8, [9, 10, [11, 12, 13, [14, 15,[16,[17,]],19]]]]]]]
    def search(l):
        for item in l:
            if type(item) is list:
                search(item)
            else:
                print(item)

    search(l)
    n = random.randint(-63,37)
    print(n)




