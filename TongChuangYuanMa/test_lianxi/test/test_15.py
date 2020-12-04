#-*- coding : utf-8 -*-
# coding: utf-8

from locust import HttpUser,task,TaskSet,between,events
import time
import random,unittest,logging
import queue
import json,sys,xlrd,openpyxl,csv
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicFunction import PublicFunction
from test_script.wode.woDeQianBao import WoDeQianBao
from Performance_Core.performance_log import loadLogger
import decimal
from faker import Faker
from common.pictures import SelectPictures
# from common.publicData import PublicData
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe
from test_script.publicscript.publicFunction import PublicFunction
from test_script.homePage import HomePage
# from report.HTMLTestRunner import HTMLTestRunner
from report.HTMLTestRunner3 import data_analyse
from locust import events
from bs4 import BeautifulSoup
# 定义用户行为
class XunBaoLiuCheng(TaskSet):
    def on_start(self):
        print("-------------------------------")
        self.header = {
            "Connection":"keep-alive",
            "Accept":"text/html, */*; q=0.01",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
            "Cookie":"SESSION=4842afed-db50-4d02-a80c-70433cf0579f; Hm_lvt_2d1cff3ad3453a1404d2ec03ab4dba21=1597391318; Hm_lpvt_2d1cff3ad3453a1404d2ec03ab4dba21=1597392255"
        }

    def setup(self):
        print('task setup')
 
    def teardown(self):
        print('task teardown')

    
    # @task
    def xunBaoShouYe(self):
        '''
        # 寻宝网首页 
        '''  
        rg_url = "/"
        rg_urlName = "寻宝网首页"
        # rg_data = {
        #     "project_id":detaill_obj_id,
        #     "num":random.randint(1,qurengou["data"]["goods"]["sale_num"]),
        #     "token":token
        # }
        with self.client.get(rg_url, headers = self.header,name = rg_urlName+rg_url,verify = False,allow_redirects=False,catch_response=True) as response:
                # rg = json.loads(response.text)
                print(response.text)
                # if "status" in rg and rg["status"] == 200:
                #     response.success()
                #     return rg
                # else:
                #     response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(rg_urlName,rg_url,rg_data,rg))
   
    # @task
    def xunBaoShouYe_list(self):
        '''
        # 寻宝网首页list 
        '''  
        rg_url = "/hot_recommend.htm?key=ajax"
        rg_urlName = "寻宝网首页列表"
        with self.client.get(rg_url, headers = self.header,name = rg_urlName+rg_url,verify = False,allow_redirects=False,catch_response=True) as response:
                print(type(response.text))
                soup = BeautifulSoup(response.text, 'html.parser')
                pplist = soup.find('section', attrs={'class': 'key_items'})
                print("=============",pplist)
                # if "status" in rg and rg["status"] == 200:
                #     response.success()
                #     return rg
                # else:
                #     response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(rg_urlName,rg_url,rg_data,rg))


    
    
    

    

    
    

    

class WebsiteUser(HttpUser):
    tasks = [XunBaoLiuCheng]
    wait_time = between(1, 3)
    host = "https://www.xunbao518.com/"

    def setup(self):
        print('locust setup')
 
    

# if __name__ == '__main__':
#     import os
#     os.system("locust -f ./test_case/liuCheng_2.py --no-web --csv=example -c 100 -r 10 --run-time 1m")
    