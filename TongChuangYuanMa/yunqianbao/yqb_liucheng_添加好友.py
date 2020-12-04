from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile
from yunqianbao.single.userMobile import user_mobile
from yunqianbao.single.publicData import PublicDataClass
from yunqianbao.pengyou.pengYouClass import PengYouClass
from common.userAgent import UserAgent

class YunQianBaoMan(TaskSet):
    def on_start(self):
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":str(int(round(time.time() * 100000))),
            "app-version":"5.5.4.1",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",  #
            "User-Agent":random.choice(UserAgent.random_userAgent()), #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded"
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        # self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        # self.publicData = PublicDataClass(self)
        self.pyobj = PengYouClass(self)
        self.login_res = self.pyobj.login(self.apikey,self.header)  #登录
        
    # @task
    def addPengYou(self):
        """
            1.登录
            2.查找用户uid
            3.添加好友

        """
        if self.login_res:
            for mobile in range(15000001200,15000001501): 
                # time.sleep(random.randint(1,3))
                print("mobile===",mobile)
                user_uid = self.pyobj.addFriends(self.apikey,self.header,self.login_res,mobile)
                if user_uid:
                    status = self.pyobj.getUserDetail(self.apikey,self.header,self.login_res,user_uid)
                    # print("status===",status)
                    if status == 200 or status == "200":
                        print("添加好友请求已发送")
            
    @task            
    def tongGuoHaoYou(self):
        tjhylist = self.pyobj.message(self.apikey,self.header,self.login_res)  
        if tjhylist:
            for itme in tjhylist:
                status = self.pyobj.passValidation(self.apikey,self.header,self.login_res,itme["id"])
                if status == 200:
                    print("通过了好友请求")



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


    

