#-*- coding : utf-8 -*-
# coding: utf-8


from locust import HttpUser,task,TaskSet,between,events
import time,queue,ast,re,requests
import random,unittest,logging
import json,sys,xlrd,openpyxl,csv
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicFunction import PublicFunction
from test_script.wode.woDeQianBao import WoDeQianBao
from Performance_Core.performance_log import loadLogger
import decimal
from common.pictures import SelectPictures
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe
from test_script.publicscript.publicFunction import PublicFunction
from test_script.homePage import HomePage
from report.HTMLTestRunner3 import data_analyse
from locust import events
from common.userAgent import UserAgent
from fontTools.ttLib import TTFont
from fontFaceDecode import FontFaceDecode
# 定义用户行为
class LiuCheng(TaskSet):
    def on_start(self):
        user_ggent = random.choice(UserAgent.random_userAgent())
        self.header = {
            "User-Agent": user_ggent,
            "Referer":"https://maoyan.com/"
        }
        filePath = "F:/proxyList.txt"
        proxyArr = self.readText(filePath) #ip代理
        self.arrProxy = []
        for pro in proxyArr:
            self.arrProxy.append({"http":pro[0]+":"+pro[1]})
        self.oldWoffPath = "E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
        self.newWoffPath = "E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file4.woff" 
        self.newXmlName = "E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/maoyan4.xml" 
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
        # print("header=====",header)
        with self.client.get(sy_url, headers = header, proxies = random.choice(self.arrProxy), verify = False,allow_redirects=False,catch_response=True) as response:
            # print("响应结果======{}".format(response.text))
            if "正在热映" in response.text:
                font_file_name = re.findall(r'//vfile.meituan.net/colorstone/(.*?).woff', response.text)[0]
                url = 'http://vfile.meituan.net/colorstone/{}.woff'.format(font_file_name)
                res = requests.get(url,headers = header)
                with open(self.newWoffPath,'wb') as f:
                    f.write(res.content)
                    print("写入成功")
                
                dictList = FontFaceDecode(self.oldWoffPath,self.newWoffPath,self.newXmlName)
                # font=TTFont(self.filename2)
                # font.saveXML("E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file4.xml")
                # newuniList=font.getGlyphOrder()[2:]
                print("33333======",dictList)
                

            # result = json.loads(response.text)
            # print(result)
                # # if "code" in result and result["code"] == 200 or result["code"] == "200": #response.status_code == 200
                # time.sleep(random.randint(1,3))
                # response.success()
                # return result

    def tff2price(para = ";",tmp_dic={},ttf_list = []):
        """
        #将爬取的字符映射为字典中的数字
        """
        tmp_return = ""
        for j in para.split(";"):
            if j != "":
                ss = j.replace("&#","0")
                for g in ttf_list:
                    if (hex(g) == ss):
                        tmp_return+=str(tmp_dic[g])
        return tmp_return

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
    