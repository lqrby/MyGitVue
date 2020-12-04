from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
<<<<<<< HEAD
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
=======
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile
from yunqianbao.single.userMobile import user_mobile
from yunqianbao.single.publicData import PublicDataClass
from yunqianbao.shouye.reMenHuoDong import ReMenHuoDong
from common.userAgent import UserAgent

class YunQianBaoMan(TaskSet):
    def on_start(self):
        # self.header ={
        #     "Connection":"keep-alive",
        #     "app-type":"android", #android
        #     "mobile-unid":str(int(round(time.time() * 100000))),
        #     "app-version":"5.5.4.1",
        #     "mobile-type":"HUAWEIALP-TL00(8.0.0)",
        #     "mobile-system":"android8.0.0",
        #     "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",  #
        #     "User-Agent":random.choice(UserAgent.random_userAgent()), #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
        #     "Content-Type":	"application/x-www-form-urlencoded"
        # }
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":str(int(round(time.time() * 100000))),
            "app-version":"5.5.4.1",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",  #
            "User-Agent":random.choice(UserAgent.random_userAgent()), #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded",
            "app-type":"ios",
            "app-version":"5.6.1",
            "device-tokens":"324bf4fa8b6d8c37b98e86f6366833fa9f2b73df648ee83e062b660f0e19ad43",
            "Content-Type":"application/x-www-form-urlencoded",
            "mobile-unid":"c8eb9ab231654cb58a14bd24f9062781",
            "mobile-system":"12.4.8",
            "User-Agent":"(iPhone; iOS 12.4.8; Scale/2.00) YunZhangBen/5.6.1",
            "mobile-type":"iPhone 6"
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        # self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        self.publicData = PublicDataClass(self)
        self.rmhd = ReMenHuoDong(self)
        self.login_res = self.publicData.login(self.apikey,self.header)  #登录
        
    
    @task            
    def tiJiaoShenQing(self):
        zmgddbres = self.rmhd.recruitingRepresentatives(self.apikey,self.header,self.login_res) #招募股东代表(申请状态)
        if zmgddbres:
            if zmgddbres["sub_status"] == "1": #申请成为股东代表
                self.rmhd.submitApplication(self.apikey,self.header,self.login_res) #提交申请
            elif zmgddbres["sub_status"] == "2": #已提交表决中
                print("已提交表决中")
            elif zmgddbres["sub_status"] == "3":#表决未通过 重新申请
                tjsqres = self.rmhd.ReSubmitApplication(self.apikey,self.header,self.login_res,zmgddbres["applyInfo"]["applyId"])  
            elif zmgddbres["sub_status"] == "8":
                print("邀请好友投票")
            elif zmgddbres["sub_status"] == "10":#已加入其它合作社
                print("已加入其它合作社")
            else:
                print("状态未知===",zmgddbres["sub_status"])
        # if tjhylist:
        #     for itme in tjhylist:
        #         status = self.pyobj.passValidation(self.apikey,self.header,self.login_res,itme["id"])
        #         if status == 200:
        #             print("通过了好友请求")



class WebsiteUser(HttpUser):
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    host = "https://tyqbapi.bankft.com/"
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   


    

