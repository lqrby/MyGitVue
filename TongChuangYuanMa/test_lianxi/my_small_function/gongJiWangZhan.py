#-*- coding : utf-8 -*-
# coding: utf-8
from locust import HttpUser,task,TaskSet,between,events
import time,ast
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

    def setup(self):
        print("是打印一次吗")

    def on_start(self):
        userAgent = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362', # Edge浏览器 版本44.18362.1.0
            'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko', # IE浏览器 版本11.175.18362.0
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0', # 火狐浏览器 x64 版本68.0
            'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0', # 火狐浏览器 x86 版本68.0
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', # Google浏览器 x64 版本75.0.3770.100
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36', # Google浏览器 x86 版本72.0.3626.121
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36', # Google浏览器 x86 版本75.0.3770.100
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36', # 2345加速浏览器 版本9.9.0.19250
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36', # 2345加速浏览器 版本10.0.0.19291
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3947.100 Safari/537.36 2345Explorer/10.0.0.19291', # 2345加速浏览器 版本10.0.0.19291
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3708.400 QQBrowser/10.4.3620.400', # QQ浏览器 版本10.4.2(3620)
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6823.400 QQBrowser/10.3.3117.400', # QQ浏览器 版本10.3.2(3117)
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400', # QQ浏览器 版本10.4.2(3587)
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36', # 360浏览器 版本10.0.1920.0
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360SE', # 360浏览器 版本10.0.1920.0 无痕
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36 QIHU 360EE', # 360极速浏览器 版本9.5.0.138
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36', # 360极速浏览器 版本11.0.2140.0
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36', # UC浏览器 版本6.2.4098.3
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0', # 搜狗高速浏览器 版本8.5.10.30358
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36', # 小智双核浏览器 版本2.0.1.12
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER', # 猎豹安全浏览器 版本6.5.115.19331.8001
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36', # QQ浏览器 版本8.9
            'Mozilla/5.0 (Linux; Android 7.1.1; NX531J) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.101 Mobile Safari/537.36', # Google浏览器 版本75.0.3770.101
            'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-cn; NX531J Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/9.5 Mobile Safari/537.36', # QQ浏览器 版本9.5.0.5050
            'Mozilla/5.0 (Linux; U; Android 7.1.1; zh-CN; NX531J Build/NMF26F) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.108 UCBrowser/12.5.5.1035 Mobile Safari/537.36', # UC浏览器 版本12.5.5.1035
            'Mozilla/5.0 (Linux; Android 7.1.1; NX531J Build/NMF26F) AppleWebKit/537.36(KHTML,like Gecko)Version/4.0 Chrome/57.0.2987.108 Mobile Safari/537.36', # Nubia浏览器 版本5.0.5.2019051016a
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044705 Mobile Safari/537.36 MMWEBID/9443 MicroMessenger/7.0.5.1440(0x27000536) Process/tools NetType/WIFI Language/zh_CN', # 微信 版本7.0.5
            'Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044705 Mobile Safari/537.36 V1_AND_SQ_7.1.0_0_TIM_D TIM/2.3.1.1834 QQ/6.5.5  NetType/WIFI WebP/0.3.0 Pixel/1080' # TIM 版本2.3.1.1834

        ]

        
        filePath = "F:/proxyList.txt"
        proxyArr = self.readText(filePath) #ip代理
        arrProxy = []
        for pro in proxyArr:
            arrProxy.append({"http":pro[0]+":"+pro[1]})
        self.proxies = arrProxy
        self.header = {
            "Connection":"keep-alive",
            "Accept":"text/html, */*; q=0.01",
            "X-Requested-With":"XMLHttpRequest",
            "User-Agent":random.choice(userAgent),
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
            "Cookie":"SESSION=4842afed-db50-4d02-a80c-70433cf0579f; Hm_lvt_2d1cff3ad3453a1404d2ec03ab4dba21=1597391318; Hm_lpvt_2d1cff3ad3453a1404d2ec03ab4dba21=1597392255"
        }

    
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

    @task
    def xunBaoShouYe_liuCheng(self):
        oneproxies = random.choice(self.proxies)
        url = "/w/sys_cs.html?c=6010&uid=523095"
        # self.client.get(url,headers = self.header)
        with self.client.get(url, headers = self.header,name = "/w/sys_cs.html",verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                print("请求成功")
            else:
                response.failure("服务器错误=={}".format(response))   

    
    
    

    

    
    

    

class WebsiteUser(HttpUser):
    tasks = [XunBaoLiuCheng]
    wait_time = between(1, 3)
    host = "https://g.ieeod0.com"

    # def setup(self):
    #     print('locust setup')
 
    

# if __name__ == '__main__':
#     import os
#     os.system("locust -f ./test_case/liuCheng_2.py --no-web --csv=example -c 100 -r 10 --run-time 1m")
    