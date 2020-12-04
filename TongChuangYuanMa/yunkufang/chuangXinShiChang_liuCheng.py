from locust import HttpUser,task,TaskSet,between,events
import time,json,random,sys,queue
<<<<<<< HEAD
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
=======
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748
from Interface.QueryUsers import queryUsers_ykf
from test_script.publicscript.publicRequestMethod import PublicRequest
from yunkufang.ykf_login import UserLogin
from yunkufang.chuangXinShiChang import ChuangXinShiChang
from gevent._semaphore import Semaphore
from yunqianbao.single.userMobile import user_mobile
all_locusts_spawned = Semaphore() #计数器
all_locusts_spawned.acquire() #计数器为0时阻塞线程 每当调用acquire()时，内置计数器-1
def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() #内置计数器+1
    print(all_locusts_spawned.release())
# events.hatch_complete += on_hatch_complete
# events.spawning_complete() += on_hatch_complete

class CXSCLiuCheng(TaskSet):
    def on_start(self):
        self.header = {
            "User-Agent":"Mozilla/5.0 (Linux; U; Android 8.0.0; zh-cn; ALP-TL00 Build/LRX22G) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Mobile Safari/537.36 YunKuFang/1.3.3",
            "mobile-system":"android8.0.0",
            "app-type":"Android",
            "app-version":"1.3.3",
            "app-version-code":"13",
            "mobile-unid":"866215038845167",
            "mobile-type":"ALP-TL00",
            "Content-Type":"application/x-www-form-urlencoded",
            "Connection":"Keep-Alive"
        }
        self.loginRes = UserLogin(self).login(self.header)
        if self.loginRes:
            # print("self.loginRes===",self.loginRes)
            self.token = self.loginRes['data']['token']
            # print("登录成功----",self.loginRes)
            # print("token----",self.token)
            self.cxscClassObj = ChuangXinShiChang(self)
            

    @task
    def liuCheng(self):
        all_locusts_spawned.wait() #在此设置了集合点
        if self.loginRes:
            cxsc_list = self.cxscClassObj.cxsc_list(self.token,self.header)  #创新市场列表
            if cxsc_list:
                detailObj = random.choice(cxsc_list["data"]["list"])
                objId = detailObj["id"]
                # objId = "b934b31641e58338da634a0fe45e1987"
                cxsc_detail = self.cxscClassObj.cxsc_detail(objId,self.token,self.header) #创新市场项目详情
                if cxsc_detail:
                    ququerenOBJ = self.cxscClassObj.quRenGou(cxsc_detail,self.token,self.header) #创新市场去认购
                    if ququerenOBJ:
                        rengou = self.cxscClassObj.renGou(ququerenOBJ,cxsc_detail['data']['id'],self.token,self.header)
                    # if not rengou:
                        # print("认购出现问题XXXX========{}".format(rengou))
        #         else:
        #             print("创新市场去认购出现问题XXXX==========".format(ququerenOBJ))
        #     else:
        #         print("创新市场列详情出现问题XXXX")
        # else:
        #     print("创新市场列表出现问题XXXX")
    


class WebsiteUser(HttpUser):
    tasks = [CXSCLiuCheng]
    wait_time = between(1, 3)
    host = "None"
    # print(host)
    # users = queryUsers_ykf(0,20) #多个用户
    # print("users===",users)
    
    # queueData = queue.Queue()
    # for user in users:
    #     print("单个用户对象=====",user)
    #     queueData.put_nowait(user)   

    # def setup(self):
    #     print('locust setup')
    mobile = user_mobile()
    users = []
    queueData = queue.Queue()
    for i in range(mobile["start"],mobile["end"]):
        # users.append(i)
        queueData.put_nowait({"mobile":i}) 
    
    # print("所有手机号====",users)
    
    # for userItem in users:
    #     queueData.put_nowait(userItem)   

    # print("queueData====",queueData)
 
    