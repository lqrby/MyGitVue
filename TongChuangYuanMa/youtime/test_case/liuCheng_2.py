#-*- coding : utf-8 -*-
# coding: utf-8
from locust import HttpUser,User,TaskSet,task,between,events
import time
import random,unittest,logging
import queue
import json,sys,xlrd,openpyxl,csv
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
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
# 定义用户行为
class LiuCheng(TaskSet):
    def on_start(self):
        # fake = Faker("zh_CN")
        # lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
        # lat = lonAndLat[0]
        # lon = lonAndLat[1]
        # LoginAndZhuCe(self).userRegister() #注册
        self.loginUserData = LoginAndZhuCe(self).userLogin() 
        if self.loginUserData:
            self.loginUser = self.loginUserData["data"]
            self.loginUser["location"]= {
                "address": '北京市通州区', #fake.company(),
                "lon": 116.63309759819349,
                "lat": 39.90490152753389
            }
            self.header = self.loginUserData['header']
        else:
            print("XXXXXXXXXX-----登录失败-----XXXXXXXX")
            self.interrupt()

        
    # def on_stop(self):
    #     print("运行结束")
    #     print(logging.getLogger('Success'))
    #     print("over*************************")


    # def setup(self):
    #     print('task setup')
 
    # def teardown(self):
    #     print('task teardown')


    @task(1) 
    def guanZhu(self):
        """
        关注
        """
        uid = 10351
        userItem = HomePage(self).fuJinDeRen_Detail(self.header,uid) #获取用户详情
        PublicFunction(self).FocusOnly(self.header,userItem)



    
    @task(1)        
    def fujinderen(self):
        '''
        # 附近的人列表》查看人员详情 》点赞 
        '''  
        # 获取附近的人列表
        fjdrList_res = HomePage(self).fuJinDeRen_list(self.header)
        fjdrList = fjdrList_res["data"]
        if fjdrList:
            for useritem in random.sample(fjdrList, random.randint(1,len(fjdrList))):
                # 查看的人详情
                userdetail_res = HomePage(self).fuJinDeRen_Detail(self.header,useritem["uid"])
                userdetail = userdetail_res["data"]
                userdetail['id'] = userdetail['uid']
                userdetail['type'] = 2
                # 给人员点赞
                PublicFunction(self).dianZan(self.header, userdetail)
        
    
    @task(1)        
    def fujindongtai(self):
        '''
        # 附近的动态列表》查看动态详情 》点赞 
        '''  
        # 获取附近动态列表
        fjdtList_res = HomePage(self).fuJinDongTai_list(self.header,self.loginUser)
        fjdtList = fjdtList_res["data"]
        if fjdtList:
            for dtitem in random.sample(fjdtList, random.randint(1,len(fjdtList))):
                # 查看动态详情
                userdtdetail_res = HomePage(self).fuJinDongTai_Detail(self.header,dtitem)
                userdtdetail = userdtdetail_res["data"]
                userdtdetail['id'] = userdtdetail['did'] 
                userdtdetail['type'] = 0
                # 给动态点赞
                PublicFunction(self).dianZan(self.header, userdtdetail)
                # 发布动态
                HomePage(self).newDynamics(self.header)

    # @task(1)        
    # def fadongtai(self):
    #     # 发布动态
    #     HomePage(self).newDynamics(self.header)

    
    @task(1)        
    def fujinjiaZhi(self):
        '''
        # 附近的价值列表》查看价值详情 》点赞 》发布价值
        '''  
        # 获取附近价值列表
        fjjzList_res = HomePage(self).fuJinJiaZhi_list(self.header,self.loginUser)
        fjjzList = fjjzList_res["data"]
        if fjjzList:
            for praisedUser in random.sample(fjjzList, random.randint(1,len(fjjzList))):
                # 查看价值详情
                jzdetail_res = HomePage(self).fuJinJiaZhi_Detail(self.header, praisedUser)
                jzdetail = jzdetail_res["data"]
                jzdetail['id'] = jzdetail['wid'] 
                jzdetail['type'] = 0
                # 给价值点赞
                PublicFunction(self).dianZan(self.header, jzdetail)
                #发布价值
                print("uid:{}".format(self.loginUser["uid"]))
                HomePage(self).publishingValue(self.header,self.loginUser["uid"])
        else:
            print("---不好意思没有数据---")

    # @task(1)        
    # def fujinjiaZhi2(self):
    #     #发布价值
    #     print("uid:{}".format(self.loginUser["uid"]))
    #     HomePage(self).publishingValue(self.header,self.loginUser["uid"])



    
    # @task(1)        
    # def myWallet(self):
    #     '''
    #     # 我的钱包》去审核 》审核 
    #     '''  
    #     # 获取审核任务
    #     if self.loginUser["userType"] == 2:
    #         qushenhe_res = WoDeQianBao(self).quShenHe(self.header)
    #         i = 1
    #         while "code" in qushenhe_res and qushenhe_res["code"] == 468:
    #             # 再次获取任务
    #             qushenhe_res = WoDeQianBao(self).quShenHe(self.header)
    #             if i>100:
    #                 # self.interrupt()
    #                 break
    #             i += i
    #         if 'code' in qushenhe_res and qushenhe_res["code"] == 200:
    #             obj = qushenhe_res["data"]["reviewId"]
    #             WoDeQianBao(self).shenHe(self.header,obj)
    #         elif 'code' in qushenhe_res and qushenhe_res["code"] == 468:
    #             print("丫的，获取任务一百次都没有任务")
    #         else: 
    #             print("xxx提交异常或审核超时xxx{}".format(qushenhe_res))
    #     else:
    #         print("----该用户没有审核权限---{}".format(self.loginUser))
    #         self.interrupt()

    @task(1)        
    def myWallet(self):
        '''
        # 我的钱包》去审核 》审核 
        '''  
        # 获取审核任务
        if self.loginUser["userType"] == 2:
            i = 1
            while i<100:
                # 获取审核任务
                qushenhe_res = WoDeQianBao(self).quShenHe(self.header)
                if 'code' in qushenhe_res and qushenhe_res["code"] == 200:
                    obj = qushenhe_res["data"]["reviewId"]
                    WoDeQianBao(self).shenHe(self.header,obj)
                    i = 1
                elif 'code' in qushenhe_res and qushenhe_res["code"] == 468:
                    print("丫的，用户{}获取不到任务{}次".format(self.loginUser,i))
                else: 
                    print("xxx{}提交异常或审核超时xxx{}".format(self.loginUser,qushenhe_res))
                i += i
        else:
            print("{}----该用户没有审核权限".format(self.loginUser))
            self.interrupt()
            

        

class WebsiteUser(HttpUser):

    tasks = [LiuCheng]
    wait_time = between(1, 3)
    host = "http://172.20.100.30"
    # host = "http://dev.ytime365.com"
    users = queryUsers(35,100) #多个用户
    # users = [{'id': 10387, 'nickname': '', 'mobile': '15000001113'}] #单个用户
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   

    def setup(self):
        print('locust setup')
 
    def teardown(self):
        print('locust teardown')
        filename='F:/jenkins_workspace/workspace/youtime/example_requests.csv'
        with open(filename,'r')as f:
            read=csv.reader(f)
            for index,info in enumerate(read):
                if index!=0:   #这里加判断
                    if info[3:4] != ['0']:
                        os.system("F:/jenkins_workspace/workspace/youtime/report/sendemail.py")

if __name__ == '__main__':
    import os
    os.system("locust -f ./test_case/liuCheng_2.py --no-web --csv=example -c 100 -r 10 --run-time 1m")
    