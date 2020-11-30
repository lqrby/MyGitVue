from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_performance")
from common.qianMing import GetDataSign
from common.single.userMobile import user_mobile
from common.userAgent import UserAgent


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


    

