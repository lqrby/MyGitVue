from locust import TaskSet
import time
import json
# 定义用户行为
class LoginRuKou(TaskSet):

    # def on_start(self):
    #     # self.userLogin()
    #     # print("执行一次")

    
    def ZhuCeMa(self):
        # 注册码
        # 将verify 设置为 False，Requests 将忽略对 SSL 证书的验证
        self.header = {"Connection":"keep-alive"}
        self.data = {
                        "qudao": "1",
                        "gid": int(time.time()),
                        "clientid": "e34f1fa5127db91fdda825528c57c9ad8",
                        "os": "9",
                        "machine": "V1829A",
                        "version": "1.0",
                        "platform": "android"
                    }
        with self.client.post("/gateway/member/macregister", data = self.data, headers = self.header, verify=False,allow_redirects=False) as response:
                if response.status_code == 200:
                    res = json.loads(response.text)
                    self.token = res['data']['token']
                    num = int(time.time())
                    self.header = {
                        "token":self.token,
                        "time":str(num),
                        "Content-Type": "application/json; charset=utf-8",
                        "User-Agent":"okhttp/2.7.5",
                        "Connection": "keep-alive",
                        "Accept-Encoding":"gzip",
                    }
                    
                else:
                    print("错误码:",response.status_code)

    def basic_setup(self):
        self.user = {
            "gid": "866215038845167",
            "code": "1234",
            "logintype": 0,
            "mobile": "15816554269",
            "pass": "c80d171b81624145618791d99107554a",
            "channel": 2
        }
        loginUser = self.userLogin(self.user)
        if loginUser and loginUser['status'] == 0:
            self.setdata = {
                "sex": 1,
                "nickname": "测试账号3",
                "birth": "19800607",
                "avatar": "https://public-tbank.oss-cn-beijing.aliyuncs.com/682e3d0a76d3bdcb1208c3092947db34.png"
            }
            with self.client.post("/gateway/member/editinfo", data = self.LoginData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
                basic_res = json.loads(response.text)
                if 'code' in basic_res and basic_res["code"] == 200:
                    # self.loginUser = basic_res["data"]
                    # self.header["token"] = basic_res["data"]["token"]
                    response.success()
                    return self.loginUser
                else:
                    response.failure("XXXX登录侯设置头像、昵称、性别、年龄失败XXXX")

        
    
    def userLogin(self,user):
        """
            登录
        """
        self.ZhuCeMa()
        self.LoginData = {
            "gid": user['gid'],
            "code": user['code'],
            "logintype": user['logintype'],
            "mobile": user['mobile'],
            "pass": user['pass'],
            "channel": user['channel']
        }
        # self.LoginData = {
        #     "gid": "866215038845167",
        #     "code": "1234",
        #     "logintype": 0,
        #     "mobile": "15001200238",
        #     "pass": "c80d171b81624145618791d99107554a",
        #     "channel": 2
        # }
        self.LoginData = json.dumps(self.LoginData)
        '''将verify 设置为 False，Requests 将忽略对 SSL 证书的验证   ,
           allow_redirects=False  禁止重定向,timeout = 20 
           catch_response=True    自定义成功失败
        '''
        with self.client.post("/gateway/member/login", data = self.LoginData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
                login_res = json.loads(response.text)
                if 'code' in login_res and login_res["code"] == 200:
                    self.loginUser = login_res["data"]
                    self.header["token"] = login_res["data"]["token"]
                    response.success()
                    return self.loginUser
                else:
                    response.failure("login fail")

    

    # '''
    # # 附近的人列表  
    # '''  
    # @task        
    # def fujin(self):
        # tasks = {WoDeQianBao:1000}

        # FuJinDeRen(self).FuJinDeRenList(self.header)
        # print("登录后的token：{}".format(self.header))
        # FuJinDeRen(self).fuJinDeRen_Detail(self.header)
        # WoDeQianBao(self).quShenHe(self.header)
        # WoDeQianBao(self).zhangDan_list(self.header)
    
    # def FuJinDeRen(self):
        
    #     self.FuJinData = {
    #         "maxage": 100,
    #         "conste": 0,
    #         "minage": 12,
    #         "location": {
    #             "address": "",
    #             "lat": 39.83877589,
    #             "lon": 116.44186175
    #         },
    #         "sex": 3,
    #         "dist": 1000000.0,
    #         "page": 1,
    #         "limit": 10
    #     }
    #     self.FuJinData = json.dumps(self.FuJinData)
    #     with self.client.post("/member/nearbylist", data = self.FuJinData, headers = self.header, verify = False, allow_redirects=False,catch_response=True) as response:
    #         fujin_res = json.loads(response.text)
    #         print(self.header,fujin_res)
    #         if 'code' in fujin_res and fujin_res["code"] == 200:
    #             response.success()
    #         else:
    #             response.failure("附近列表 fail")