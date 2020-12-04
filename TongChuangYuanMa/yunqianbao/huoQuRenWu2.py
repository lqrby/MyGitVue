from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
import ast
# from requests_toolbelt import MultipartEncoder
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile

class ComTasks(TaskSet):
    def on_start(self):
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":"866215038845168",
            "app-version":"5.4.91",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "",  #AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded",
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        self.userData_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/login.txt"
        struser = WriteAndReadTextFile().readAll_txt(self.userData_path)
        self.user_dict = ast.literal_eval(struser)
    
    @task
    def main_entrance(self):
        """"
        进入获取任务页
        
        """
        url = "v2/new-year20/online-period"
        canshu_data = {
            "access_token":self.user_dict["access_token"],
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        # print("userDict======={}".format(canshu_data),)
        sign = GetDataSign().sign_body(url,canshu_data, self.apikey)
        canshu_data["sign"] = sign
        #进入获取任务页面
        hqrw_res = PublicRequest(self).requestMethod(url,canshu_data,self.header)
        return hqrw_res
        # if renwu_res and renwu_res["totalTask"] > 0:
        #     print("*******************************jin ru ren wu ************************")
        
    @task
    def huoQuTask(self):
        """"
        获取任务
        
        """
        rw_url = "v2/user/card-status"
        renwu_data = {
            "access_token":self.user_dict["access_token"],
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(rw_url,renwu_data, self.apikey)
        renwu_data["sign"] = sign
        #进入获取任务页面
        renwu_res = PublicRequest(self).requestMethod(rw_url,renwu_data,self.header)
        if not renwu_res:
            print("XXXXXXXXXXXXXX获取任务失败，您未实名或实名信息在审核中XXXXXXXXXXXXX{}".format(renwu_res))
        return renwu_res


