from locust import HttpUser,User,TaskSet,task,between,events
import time
import queue
import json,sys
import random
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from Interface.QueryUsers import queryUsers
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe

class FaXiaoXi(TaskSet):
    '''
    # 发消息
    '''        
    def on_start(self):
        self.loginResponse = LoginAndZhuCe(self).userLogin()
        self.header = self.loginResponse["header"]
        self.loginUser = self.loginResponse["data"]
        self.countter = 0   
        self.txt = "4.14测试消息！=" 
    '''
    # 获取群组列表
    '''  
     
    def qunZu_list(self):
        #群组列表
        self.qunzuData = {
                "content":""
            }
        # print("token",self.header)
        self.qunzuData = json.dumps(self.qunzuData)
        with self.client.post(":9090/group/list", data = self.qunzuData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
            time.sleep(random.uniform(0.8,3))
            # print("6363636363:{}".format(response))
            qunzulist = json.loads(response.text)
            if 'code' in qunzulist and qunzulist["code"] == 200:
                # print("群组列表是:{}".format(qunzulist))
                response.success()
                return qunzulist["data"]
            else:
                print("XXX获取群组列表错误XXX0{}".format(qunzulist))
                response.failure("XXX获取群组列表失败XXX{}".format(qunzulist))

    
    # @task(1)
    def qunFaXiaoXi(self):
        '''
        多个群组连续发消息
        '''
        self.countter = self.countter+1
        qunzuList = self.qunZu_list()
        if len(qunzuList) > 0:
            # number = random.randint(1,100)
            number = 5
            count = 5
            text = {"txt":self.txt+"{}".format(str(self.countter))}
            uid= self.loginUser['uid']
            nickname = self.loginUser['nickname']
            if len(qunzuList) > number :
                for i in range(number): 
                    fujinItem = random.choice(qunzuList)
                    self.xiaoxiData = {
                        "count":count,
                        "bType":1,
                        "cType":1,
                        "ext":text,
                        "fId":uid, #登录用户的id
                        "fNm":nickname, #登录用户的名字
                        "fRely":0,
                        "tId":fujinItem['groupId'], #群id
                        "tNm":fujinItem['gname'] #群名称
                        }  
                    self.xiaoxiData = json.dumps(self.xiaoxiData)
                    with self.client.post("/group/admin/groupChat", data = self.xiaoxiData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
                        time.sleep(random.randint(1,3))
                        qzlb_res = response.text
                        if 'success' in qzlb_res:
                            response.success()
                        else:
                            print("XXX发送群消息失败XXX{}".format(qzlb_res))
                            response.failure("XXX发送群消息失败XXX{}".format(qzlb_res))
            else:
                for i,item in enumerate(qunzuList):
                    self.xinxiData = {
                        "count":count,
                        "bType":1,
                        "cType":1,
                        "ext":text,
                        "fId": uid, #登录用户的id
                        "fNm":nickname, #登录用户的名字
                        "fRely":0,
                        "tId":item['groupId'], #群id
                        "tNm":item['gname']}  #群名称
                    self.xinxiData = json.dumps(self.xinxiData)
                    with self.client.post("/group/admin/groupChat", data = self.xinxiData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
                        time.sleep(random.randint(1,3))
                        qzlb_res = response.text
                        if 'success' in qzlb_res:
                            response.success()
                            # self.interrupt()
                        else:
                            print("XXX发送群消息失败XXX222222,{}".format(qzlb_res))
                            response.failure("XXX发送群消息失败XXX222222,{}".format(qzlb_res))
        else:
            print("本尊通讯录暂时还没有群聊！！！")
        

    
    @task(1)
    def danQunFaXiaoXi(self):
        '''
        单个群连续发消息
        '''
        self.countter = self.countter+1
        self.xiaoxiData = {
            "bType":1,
            "cType":1,
            "ext":{"txt":self.txt+"{}".format(str(self.countter))},
            "fId":self.loginUser['uid'], #登录用户的id
            "fNm":self.loginUser['nickname'], #登录用户的名字
            "fRely":0,
            "tId":20037, #群id
            "tNm":"红满天1我的群" #群名称
            }  
        self.xiaoxiData = json.dumps(self.xiaoxiData)
        with self.client.post("/group/admin/groupChat", data = self.xiaoxiData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
            time.sleep(random.randint(1,3))
            qzlb_res = response.text
            if 'success' in qzlb_res:
                response.success()
                # self.interrupt()
            else:
                print("XXX发送群消息失败XXX,{}".format(qzlb_res))
                response.failure("XXX发送群消息失败XXX,{}".format(qzlb_res))
        

class WebsiteUser(HttpUser):
    tasks = [FaXiaoXi]
    wait_time = between(1, 3)
    host = "http://172.20.100.30"     
    users = queryUsers() #多个用户
    queueData = queue.Queue()
    for userItem in users:
        queueData.put_nowait(userItem) 