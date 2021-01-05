'''
version: V2.0
Author: 学海无涯任我游
Date: 2020-12-28 15:30:10
LastEditors: 学海无涯任我游
LastEditTime: 2020-12-28 15:36:11
'''
from functools import reduce
def myfunc(x,y):
    return x*y

print(reduce(myfunc,[1,2,3,4],2))

