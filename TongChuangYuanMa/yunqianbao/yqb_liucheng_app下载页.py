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
from yunqianbao.single.publicData import PublicDataClass
from yunqianbao.single.userMobile import user_mobile
from yunqianbao.pengyou.pengYouClass import PengYouClass
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
            "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding":"gzip, deflate",
            "if-none-match":"5f8ea592-c2a"
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        
        
    @task
    def xiaZaiYan(self):
        """
            app下载页面
        """
        openlist_url = "text/download"
        openlist_data = {}
        with self.client.get(openlist_url,data=openlist_data,headers=self.header,verify=False,allow_redirects=False,catch_response=True) as response:
            print(response)
            if "200" in response:
                print("6666666666=",response)
            else:
                print(response.text)
            return response
            
                



class WebsiteUser(HttpUser):
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    host = "https://m.pmm2020.com/"
    # users = queryUsers() #多个用户
    # mobile = user_mobile()
    # users = []
    # for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
    #     users.append(i)
    # queueData = queue.Queue()
    # for userItem in users:
    #     queueData.put_nowait(userItem)   


    

