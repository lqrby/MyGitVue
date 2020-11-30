from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
# from case.classApiTest import ClassTestCase
from case.class_api_test import ZFAclassTestCase
from common.qianMing import GetDataSign
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
        
        
        self.access_token = ""
        self.last_response = ""
        self.ctc = ZFAclassTestCase(self)
        app_name = "云账本"
        host_key = "yzb_test_host"
        pz_obj = self.ctc.loadConfigByAppAndKey(app_name,host_key)
        self.api_key = pz_obj["api_key"]
        #获取接口的域名https://tyqbapi.pmm2020.com            return{'id': 1, 'name': '云账本', 'dict_key': 'yzb_test_host', 'dict_value': 'https://tyqbapi.pmm2020.com'}
        # self.api_host_obj = self.ctc.loadConfigByAppAndKey(app_name,host_key)
        #根据用例id登录
        case_id = 5
        case = self.ctc.findCaseById(case_id)
        try:
            #执行用例
            response = self.ctc.runCase(case,self.last_response, self.api_key)
            
            #断言判断
            assert_msg = self.ctc.assertResponse(case, response)
            if assert_msg.get("is_pass") == True:
                response.success()
                self.login_response = json.loads(response.text)
                self.access_token = self.login_response["data"]["access_token"]
                self.last_response = response.text
                print("响应成功self.access_token====",self.access_token)
            else:
                response.failure("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
                print("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
        except Exception as e:
            print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))




    @task
    def userShiMing(self):
        """
            1.登录
            2.首页
            3.实名
            4.实名状态

        """
        caseListId = [79,80]
        # self.ctc.runAllCase(caseListId, api_host_obj = self.api_host_obj, access_token = self.access_token, last_response=self.last_response)
        caseArr = []
        for case_id in caseListId: #需要执行的所有用例id
            case = self.ctc.findCaseById(case_id)
            caseArr.append(case)
        print("cases==",caseArr)
        #循环执行用例
        for case in caseArr:
            try:
                #执行用例
                response = self.ctc.runCase(case,self.last_response, self.api_key)
                print("response111===",response)
                #断言判断
                assert_msg = self.ctc.assertResponse(case, response)
                print("断言====",assert_msg)
                if assert_msg.get("is_pass") == True:
                    response.success()
                    self.last_response = response.text
                    print("响应成功===self.last_response=",self.last_response)
                else:
                    response.failure("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
                    print("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
                #更新结果，储存数据库
                # rows = self.updateResultByCaseId(reponse, assert_msg["is_pass"], assert_msg["msg"], case["id"])
                # if rows:
                #     print("更新完成")
                # else:
                #     print("XXXXXX更新失败！XXXXXX")
            except Exception as e:
                print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

        
        
        



class WebsiteUser(HttpUser):
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    # host = "https://tyqbapi.pmm2020.com/"
    app_name = "云账本"
    host_key = "yzb_test_host"
    pz_obj = ZFAclassTestCase(TaskSet).loadConfigByAppAndKey(app_name,host_key)
    host = pz_obj["dict_value"]
    print("host====",host)
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


