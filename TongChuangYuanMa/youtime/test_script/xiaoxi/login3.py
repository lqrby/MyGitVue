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

    
    
    def userLogin(self):
        """
            登录
        """
        self.ZhuCeMa()
        # self.LoginData = {
        #     "gid": user['gid'],
        #     "code": user['code'],
        #     "logintype": user['logintype'],
        #     "mobile": user['mobile'],
        #     "pass": user['pass'],
        #     "channel": user['channel']
        # }
        self.LoginData = {
            "gid": "866215038845167",
            "code": "1234",
            "logintype": 0,
            "mobile": "15001200238",
            "pass": "c80d171b81624145618791d99107554a",
            "channel": 2
        }
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

    

    