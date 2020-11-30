from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_performance")
from common.qianMing import GetDataSign
from common.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile
from common.single.publicData import PublicDataClass
from common.single.userMobile import user_mobile
from common.pengyou.pengYouClass import PengYouClass
from common.userAgent import UserAgent
from gevent._semaphore import Semaphore
all_locusts_spawned = Semaphore() #计数器
all_locusts_spawned.acquire() #计数器为0时阻塞线程 每当调用acquire()时，内置计数器-1

# def on_hatch_complete(**kwargs):
#     all_locusts_spawned.release() #内置计数器+1

# events.hatch_complete += on_hatch_complete


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
            "Content-Type":	"application/x-www-form-urlencoded",
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        # self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        self.publicData = PublicDataClass(self)
        self.PengYou = PengYouClass(self)
        self.login_res = self.PengYou.login(self.apikey,self.header)  #登录
        
    @task
    def userShiMing(self):
        """
            1.登录
            2.实名状态
            3.抢红包
            4.打开红包
        """
        # print("开始集合")
        # all_locusts_spawned.wait(timeout=60) #在此设置了集合点
        # print("集合释放")
        if self.login_res:
            taskdata = self.publicData.getUserType(self.apikey,self.header,self.login_res) #查看实名状态/获取任务
            
                



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


    

