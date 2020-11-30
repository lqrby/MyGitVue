from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_pressure")
from common.userAgent import UserAgent
from case.class_api_test import ZFAclassTestCase
from common.qianMing import GetDataSign
from common.userMobile import user_mobile
from common.userAgent import UserAgent

class YunQianBaoMan(TaskSet):
    def on_start(self):
        self.headers ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":str(int(time.time() * 100000)),
            "app-version":"5.5.4.1",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-"+str(int(time.time() * 1000)),  #
            "User-Agent": random.choice(UserAgent().random_userAgent()) #"Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
        }
        
        
        self.loginData = ""
        self.last_response = {}
        self.ctc = ZFAclassTestCase(self)
        app_name = "云账本"
        host_key = "yzb_test_host"
        self.api_host_obj = self.ctc.loadConfigByAppAndKey(app_name,host_key)
        # self.api_key = self.api_host_obj["api_key"]

        #获取接口的域名https://tyqbapi.pmm2020.com            return{'id': 1, 'name': '云账本', 'dict_key': 'yzb_test_host', 'dict_value': 'https://tyqbapi.pmm2020.com'}
        # self.api_host_obj = self.ctc.loadConfigByAppAndKey(app_name,host_key)
        #根据用例id登录
        case_id = 5
        case = self.ctc.findCaseById(case_id)
        try:
            #执行用例
            response_text = self.ctc.login(case,self.headers,self.last_response, self.api_host_obj, self.loginData)
            if response_text:
                self.loginData = json.loads(response_text)["data"]
                print("登录返回值=====",self.loginData["access_token"],self.loginData)
                self.last_response = json.loads(response_text)
            else:
                print("登录断言失败--url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"], response_text))
        except Exception as e:
            print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

        caseListId = [79,80,62,111,14,15,16,17,19,11,12,20,22,23,24,25]
        # caseListId = [15,16,11,12,14]
        self.caseArr = []
        for case_id in caseListId: #需要执行的所有用例id
            case = self.ctc.findCaseById(case_id)
            self.caseArr.append(case)


    @task
    def userShiMing(self):
        """
            1.登录
            2.首页
            3.实名
            4.实名状态

        """
        print("kai shi ")
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
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    app_name = "云账本"
    host_key = "yzb_test_host"
    pz_obj = ZFAclassTestCase(TaskSet).loadConfigByAppAndKey(app_name,host_key)
    host_values = json.loads(pz_obj["dict_value"])
    host = host_values["native_host"]
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   


    




