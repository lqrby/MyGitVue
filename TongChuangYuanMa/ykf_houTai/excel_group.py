import time,json,random,sys,queue,re
import openpyxl,xlrd,ast
from bs4 import BeautifulSoup
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
# from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicRequestMethod import PublicRequest
# from yunkufang.ykf_login import UserLogin
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from requests_toolbelt.multipart.encoder import MultipartEncoder



class ExcelGroup:

    def readExcel(filepath):
        """
        打开excel表，读取数据并转换成数组对象
        """
        book = xlrd.open_workbook(filepath)
        #找到sheet页
        table = book.sheet_by_name("任保玉")
        #获取总行数总列数
        row_Num = table.nrows
        col_Num = table.ncols
        s =[]
        key =table.row_values(0)# 这是第一行数据，作为字典的key值
        if row_Num <= 1:
            print("没数据")
        else:
            j = 1
            for i in range(row_Num-1):
                d ={}
                values = table.row_values(j)
                for x in range(col_Num):
                    # 把key值对应的value赋值给key，每行循环
                    d[key[x]]=values[x]
                j+=1
                # 把字典加到列表中
                s.append(d)
            return s

    def merge_dict(detail_list):
        '''
        根据手机号分组数据
        '''
        goods_ids = set([i.get('收件人手机') for i in detail_list])
        # print(goods_ids)
        detail_list_group = []
        for x in goods_ids:
            temp = []
            for y in detail_list:
                if y.get('收件人手机') == x:
                    temp.append(y)
            if temp:
                detail_list_group.append(temp)
        return detail_list_group

    def writeText(filePath,groupList):
        """
        把数据写入txt文件
        """
        with open(filePath, 'w') as f:
            f.write(str(groupList))
            print("分组数据写入成功啦")

    def readText(filePath):
        """
        读取txt文件内的数据
        """
        dictdata = {}
        with open(filePath, "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            # print("data==",data)

            dictdata = ast.literal_eval(data)
            print("读取txt文件内的数据=====",dictdata)
        return dictdata


    


    

    
        

   

  

    

