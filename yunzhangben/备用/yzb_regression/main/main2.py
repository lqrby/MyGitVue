from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
from case.classApiTest import ClassTestCase
from common.qianMing import GetDataSign
from common.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile
from common.publicData import PublicDataClass
from common.userMobile import user_mobile
from common.userAgent import UserAgent

class YunQianBaoMan(TaskSet):
    def on_start(self):
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":"1603432610",#str(int(round(time.time() * 100000))),
            "app-version":"5.5.4.1",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",  #
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",#random.choice(UserAgent.random_userAgent()), #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded"
        }
        # self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        self.ctc = ClassTestCase(self)
        self.access_token = ""
        self.obj = {}
        
    @task
    def userShiMing(self):
        """
            1.登录
            2.首页
            3.实名
            4.实名状态

        """
        app_name = "云账本"
        host_key = "yzb_test_host"
        caseListId = [5]
        for case_id in caseListId:
            self.ctc.runAllCase(app_name, case_id=case_id, host_key=host_key)
            # print("6666666")
        # if res:
        #     res2 = self.ctc.runCase(case,79)
        #     if res2:
        #         res3 = self.ctc.runCase(case,80)

        # for id in appListId：

        #     self.ctc.runAllCase(app_name, host_key="None", appListId = appListId)
        # publicData = PublicDataClass(self)
        # self.login_res = publicData.login(self.apikey,self.header)  #登录
        # if self.login_res:
        #     # is_safe = self.publicData.index(self.apikey,self.header,self.login_res)  #获取首页
        #     # self.publicData.setMiBao(self.apikey, self.header,self.login_res,is_safe) # 设置密保
        #     taskdata = publicData.getUserType(self.apikey,self.header,self.login_res) #查看实名状态/获取任务
            # if taskdata == 5:
            #     print("进入朋友列表")
            #     ltjllist = publicData.pengYou(self.apikey,self.header,self.login_res)
                # if len(ltjllist)>0:
                #     #获取聊天页成员list
                #     reslist = publicData.getInfo(self.apikey,self.header,self.login_res,ltjllist[0])
                #     gift_id = 84
                #     aicnum = publicData.robRedEnvelopes(self.apikey,self.header,self.login_res,gift_id)
                #     if aicnum["nums"]>"0":
                #         redEnvelopes = publicData.openRedEnvelopes(self.apikey,self.header,self.login_res,gift_id,ltjllist[0])
                #         print("抢到{}个aic".format(redEnvelopes["aic"]))
            



class WebsiteUser(HttpUser):
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    host = "https://tyqbapi.pmm2020.com/"
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   


    




# if __name__ == "__main__":
#     '''
#             5:回答密保问题
#             79:系统公告
#             80:系统公告详情
#         '''
#     listId = [5,79,80]
#     app = ZFAclassTestCase()
#     app.runAllCase("云账本","yzb_test_host")


