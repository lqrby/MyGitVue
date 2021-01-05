from locust import HttpUser,task,TaskSet,between,events,LoadTestShape
from locust.contrib.fasthttp import FastHttpUser
import random,time,json
import base64
import sys
import queue
# from multiprocessing import Queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunkufang/ykf_pressure")
from common.userAgent import UserAgent
from case.class_api_test import ZFAclassTestCase
from case.qianMing import GetDataSign
from common.userMobile import user_mobile
from common.userAgent import UserAgent
from gevent._semaphore import Semaphore
# all_locusts_spawned = Semaphore()
# all_locusts_spawned.acquire() #减1

# def on_spawning_complete(**kwargs):
#     all_locusts_spawned.release() #创建钩子方法

# events.spawning_complete.add_listener(on_spawning_complete) #挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class YunQianBaoMan(TaskSet):
    def on_start(self):
        self.headers ={
            "Connection":"keep-alive",
            "app-type":"android",
            "mobile-unid":str(int(time.time() * 100000)),
            "app-version":"2.0.1",
            "app-version-code":"19", 
            "mobile-type":"ALP-TL00" + str(int(time.time() * 1000)),
            "mobile-system":"android9",
            "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-"+str(int(time.time() * 1000)),  #
            "User-Agent": random.choice(UserAgent().random_userAgent()) #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
        }
        
        
        self.loginData = ""
        self.last_response = {}
        self.ctc = ZFAclassTestCase(self)
        app_name = "云库房"
        host_key = "ykf_dev_host"
        self.api_host_obj = self.ctc.loadConfigByAppAndKey(app_name,host_key)
        #获取接口的域名https://tyqbapi.pmm2020.com            return{'id': 1, 'name': '云账本', 'dict_key': 'yzb_test_host', 'dict_value': 'https://tyqbapi.pmm2020.com'}
        #根据用例id登录
        case_id = 120
        case = self.ctc.findCaseById(case_id)
        try:
            #执行用例
            response_text = self.ctc.login(case,self.headers,self.last_response, self.api_host_obj, self.loginData)
            if response_text:
                self.loginData = json.loads(response_text)["data"]
                # print("登录返回值=====",self.loginData["token"],self.loginData)
                self.last_response = json.loads(response_text)
            else:
                print("登录断言失败--url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"], response_text))
        except Exception as e:
            print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

        # caseListId = [121,122,123,127] #首页接口
        caseListId = [129] #首页接口
        self.caseArr = []
        for case_id in caseListId: #需要执行的所有用例id
            case = self.ctc.findCaseById(case_id)
            self.caseArr.append(case)
        # all_locusts_spawned.wait()
        


    @task
    def userShiMing(self):
        
        # print("开始")
        #循环执行用例
        for case in self.caseArr:
            try:
                #执行用例
                response_text = self.ctc.runCase(case,self.headers,self.last_response, self.api_host_obj, self.loginData)
                if response_text == 0:
                    print("用例id-{}-未执行，原因:该用例依赖的前置用例列表为空".format(case["id"]))
                    continue
                if response_text:
                    self.last_response = json.loads(response_text)
                else:
                    print("断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response_text))
            except Exception as e:
                print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

        
        
        



class WebsiteUser(HttpUser):
    @events.test_start.add_listener
    def on_test_start(self,**kw):
        print("test is starting")
        
    tasks = [YunQianBaoMan]
    wait_time = between(0.1, 0.5)
    app_name = "云库房"
    # host_key = "ykf_test_host"
    host_key = "ykf_dev_host"
    pz_obj = ZFAclassTestCase(TaskSet).loadConfigByAppAndKey(app_name,host_key)
    host_values = json.loads(pz_obj["dict_value"])
    host = host_values["native_host"]
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    # queueData = Queue()
    queueData = queue.Queue()
    for userItem in users:
        print("yonghu---",userItem)
        queueData.put_nowait(userItem)  
    print("用户队列=========",queueData)


    




