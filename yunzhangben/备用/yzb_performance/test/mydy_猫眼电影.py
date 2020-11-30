#-*- coding : utf-8 -*-
# coding: utf-8
from locust import HttpUser,task,TaskSet,between,events
import time,queue,ast
import random,unittest,logging
import json,sys,xlrd,openpyxl,csv
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_performance")
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicFunction import PublicFunction
from test_script.wode.woDeQianBao import WoDeQianBao
from Performance_Core.performance_log import loadLogger
import decimal
from common.pictures import SelectPictures
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe
from test_script.publicscript.publicFunction import PublicFunction
from test_script.homePage import HomePage
# from report.HTMLTestRunner import HTMLTestRunner
from report.HTMLTestRunner3 import data_analyse
from locust import events
from common.userAgent import UserAgent
from fontTools.ttLib import TTFont

# 定义用户行为
class LiuCheng(TaskSet):
    def on_start(self):
        user_ggent = random.choice(UserAgent.random_userAgent())
        self.header = {"User-Agent": user_ggent}
        filePath = "F:/proxyList.txt"
        proxyArr = self.readText(filePath) #ip代理
        self.arrProxy = []
        for pro in proxyArr:
            self.arrProxy.append({"http":pro[0]+":"+pro[1]})
        # self.proxies = random.choice(arrProxy)
        # print("self.proxies====",self.proxies)
    # def setup(self):
    #     print('task setup')
 
    # def teardown(self):
    #     print('task teardown')
    def readText(self,filePath):
        """
        读取txt文件内的数据
        """
        dictdata = {}
        with open(filePath, "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            dictdata = ast.literal_eval(data)
            # print("读取txt文件内的数据=====",dictdata)
        return dictdata

    @task(1) 
    def myList(self):
        """
        猫眼首页
        """
        sy_url = "/"
        header = {"User-Agent": random.choice(UserAgent.random_userAgent())}
        print("header=====",header)
        with self.client.get(sy_url, headers = header, proxies = random.choice(self.arrProxy), verify = False,allow_redirects=False,catch_response=True) as response:
            # print("响应结果======{}".format(response.text))
            print("111111")
            
            if "正在热映" in response.text:

                    print("9999999",response.text)
            else:
                print("33333",type(response),response)
            # result = json.loads(response.text)
            # print(result)
                # # if "code" in result and result["code"] == 200 or result["code"] == "200": #response.status_code == 200
                # time.sleep(random.randint(1,3))
                # response.success()
                # return result


class WebsiteUser(HttpUser):
    tasks = [LiuCheng]
    wait_time = between(1, 3)
    host = "https://maoyan.com"
    # host = "http://dev.ytime365.com"
    # users = queryUsers(35,100) #多个用户
    # # users = [{'id': 10387, 'nickname': '', 'mobile': '15000001113'}] #单个用户
    # queueData = queue.Queue()
    # for userItem in users:
    #     queueData.put_nowait(userItem)   

    
    

# if __name__ == '__main__':
#     import os
#     os.system("locust -f ./test_case/liuCheng_2.py --no-web --csv=example -c 100 -r 10 --run-time 1m")
    