import random
from random import choice
import string
def Unicode(n):
    s = ""
    for i in range(n):
        val = random.randint(0x4e00, 0x9fbf)
        x = chr(val)
        s = s + x
    return s

def GBK2312(n):
    s = ""
    for i in range(n):
        head = random.randint(0xb0, 0xf7)
        body = random.randint(0xa1, 0xfe)
        val = '{0:x}{1:x}'.format(head, body)
        str = bytes.fromhex(val).decode('gb2312')
        s = s + str
    return s

def phone_num():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
           '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits,7))
    res = start+end
    return res

def tecphone_num():
    num_start = ['134', '135', '136', '137', '138', '139', '150', '151', '152', '158', '159', '157', '182', '187', '188',
           '147', '130', '131', '132', '155', '156', '185', '186', '133', '153', '180', '189']
    start = random.choice(num_start)
    end = ''.join(random.sample(string.digits,8))
    res = start+end
    return res

def Generate(n):
    a = ["我觉得","我是","差不多吧","可能","我认为","这样就行了","嗯嗯","可以有","哈哈哈"]
    s = ""
    for i in range(n):
        x = choice(a)
        s = s + x
    return s







if __name__ == '__main__':
    a = tecphone_num()
    print(a)
