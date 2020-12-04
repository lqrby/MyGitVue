from locust import HttpUser,task,TaskSet,between,events
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from yunqianbao.single.huoQuRenWu import ComTasks
from yunqianbao.single.publicData import PublicDataClass
from yunqianbao.single.userMobile import user_mobile


class YunQianBaoMan(TaskSet):
    def Setups(self):
        pass
    
    def TearDowns(self):
        pass
    def on_start(self):
        self.header ={
            "Connection":"keep-alive",
            "app-type":"android", #android
            "mobile-unid":str(int(round(time.time() * 100000))),
            "app-version":"5.4.91",
            "mobile-type":"HUAWEIALP-TL00(8.0.0)",
            "mobile-system":"android8.0.0",
            "device-tokens": "",  #AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
            "Content-Type":	"application/x-www-form-urlencoded",
        }
        self.apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
        self.sfz_path = "F:/myTestFile/TestObject/YouTime/yunqianbao/static/shenfenzheng.txt"
        self.public_Data = PublicDataClass(self)
        self.login_res = self.public_Data.login(self.apikey,self.header)  #登录
        
        
    # def on_logout(self):
    #     self.public_Data.userLogout(self.apikey,self.header,self.login_res)
        

    @task
    def huoqurenwu(self):
        is_safe = self.public_Data.index(self.apikey,self.header,self.login_res)  #获取首页
<<<<<<< HEAD
        # if is_safe:
        #     self.public_Data.setMiBao(self.apikey, self.header,self.login_res,is_safe) # 设置密保
=======
        if is_safe:
            self.public_Data.setMiBao(self.apikey, self.header,self.login_res,is_safe) # 设置密保
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748
        # taskdata = self.public_Data.getUserType(self.apikey,self.header,self.login_res) #获取用户实名状态
        # if taskdata["type"] == 3:
        #     print("实名认证信息已提交====待审核===={}".format(self.login_res))
        # elif taskdata["type"] == 1:
        #     self.public_Data.shiMing(self.apikey,self.header,self.login_res,self.sfz_path) #实名认证
        # else:
        #     pass
        # taskdata = self.public_Data.getUserType(self.apikey,self.header,self.login_res) #查询用户实名状态
        # if taskdata and taskdata["type"] == 5:
        #     dqres = self.public_Data.getDangQiId(self.apikey,self.header,self.login_res) #获取当期id
        #     self.public_Data.comTask(self.apikey,self.header,self.login_res,dqres["periodId"]) #进入获取任务页
        #     self.public_Data.getUserType(self.apikey,self.header,self.login_res) #实名状态
        #     queryRes = self.public_Data.queryPaymentPassword(self.apikey,self.header,self.login_res) #查询用户是否设置了交易密码
        #     if not queryRes["paypwd_set"]:
        #         self.public_Data.setPaymentPassword(self.apikey,self.header,self.login_res) #设置支付密码
        #     money = self.public_Data.selectGoldShares(self.apikey,self.header,self.login_res) #查询账户余额
        #     if money:
        #         self.public_Data.paymentTaskMoney(self.apikey,self.header,self.login_res) #支付任务押金
                
        


    
class WebsiteUser(HttpUser):
    tasks = [YunQianBaoMan]
    wait_time = between(1, 3)
    host = "https://tyqbapi.pmm2020.com/"
    
    # users = queryUsers() #多个用户
    mobile = user_mobile()
    # mobile = PublicDataClass(TaskSet).userMobile()
    users = []
    for i in range(mobile["start"],mobile["end"]): #(15001200238,15001200239): #
        users.append(i)
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem)   


    # class WebUserLocust(Locust):
    # weight = 3
    # ...

    # class MobileUserLocust(Locust):
    # weight = 1

