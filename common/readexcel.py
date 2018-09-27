# coding:utf-8
import xlrd
class Excelread():
    def __init__(self, excelPath, sheetName="Sheet"):#初始化方法（实例化时会生成这些属性）
        self.data = xlrd.open_workbook(excelPath)#打开路径下的excel
        self.table = self.data.sheet_by_name(sheetName)#打开excel的第一个sheet页
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        # 获取总行数
        self.rowNum = self.table.nrows
        # 获取总列数
        self.colNum = self.table.ncols

    def dict_data(self):#读取excel中sheet中的值并生成一个字典
        if self.rowNum <= 1:#如果sheet中行数小于等于1
            print("总行数小于1")#sheet中没数据（小于1），或者只有列名（等于1）
        else:
            r = []#定义一个空列表，存放字典（每一行的数据）
            j = 1
            for i in list(range(self.rowNum-1)):#range（10-1）就是range（9），就是取值0、1、2、3、4、5、6、7、8，list(range(9))就是转换成列表[0,1,2,3,4,5,6,7,8]
                s = {}#定义一个空字典，存放每一行形成的字典

                s['rowNum'] = i+2# 从第二行取对应values值，给字典赋值{'rowNum':i+2}
                values = self.table.row_values(j)#从第二行取excel的所有值（一行有好几个值，见api.xlsx）
                for x in list(range(self.colNum)):#根据一行多少列循环取每一列的值
                    s[self.keys[x]] = values[x]#self。keys[x]取的是第一行的x列的值作为key，values[x]取的是第j行的x列作为value，形成字典里的值
                r.append(s)#将生成的一行数据的字段加进列表
                j += 1#取下一行的所有值
            return r
    #总结：第一个循环循环的每一行，第二个内循环循环的某行的每一列，形成一个字典，并组合成一个列表，比如[{a:1,b:11,c:111},{a:2,b:22,c:222},{a:3,b:33,c:333}]，excel存值如
    # a  b  c
    # 1  11 111
    # 2  22 222
    # 3  33 333

if __name__ == "__main__":
    filepath = "C:\\Users\\Administrator\\PycharmProjects\\Kesgotd_screen_CountScore\\case\\write.xlsx"
    sheetName = "Sheet"
    data = Excelread(filepath, sheetName)
    print(data.dict_data()[0]["总分"])
    print(type(data.dict_data()[0]["总分"]))