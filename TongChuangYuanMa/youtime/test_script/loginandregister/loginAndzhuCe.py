from locust import TaskSet
import time,json,random
import queue
from requests_toolbelt import MultipartEncoder
import sys
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from test_script.publicscript.publicRequestMethod import PublicRequest
from Interface.Captcha import returnCaptcha




class LoginAndZhuCe(TaskSet):

    def findCaptcha(self,mobile,header):
        '''
        发送短信验证码
        '''
        captcha_urlName = "获取短信验证码"
        captcha_url = "/gateway/member/smscode"
        captcha_data = {
            "mobile": str(mobile),
            "type": 0
        }
        return PublicRequest(self).publicRequest(captcha_url,captcha_urlName,captcha_data,header)  
        



    def userRegister(self):
        """
            注册
        """
        self.ZhuCeMa()
        try:
            # mobile = self.locust.queueMobile.get()  #获取队列里的数据
            mobile = "15000001113"  #获取队列里的数据
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        # if self.findCaptcha(mobile,self.header):
        #     i = 0
        #     time.sleep(5)
        #     code = returnCaptcha(self.header["token"])
        #     while (code == False):
        #         time.sleep(random.randint(1,5))
        #         code = returnCaptcha(self.header["token"])
        #         print("第一次没获取到，再次获取的验证码是：{}".format(code))
        #         i += 1
        #         if i>4:
        #             print("4444")
        #             print("丫的没发送短信验证码")
        #             code = "1234"
        #             break
        registerData = {
            "password": "c80d171b81624145618791d99107554a",
            "code": "",#str(code),
            "gid": "866215038845167", #str(int(round(time.time() * 100000)))
            "mobile": str(mobile),
            "type":2,
            "resource":1
        }
        registerUrl = "/gateway/member/mobileregister"
        registerUrlName = "注册"
        '''将verify 设置为 False，Requests 将忽略对 SSL 证书的验证   ,
        allow_redirects=False  禁止重定向,
        timeout = 20   超时
        catch_response=True    自定义成功失败
        '''
        with self.client.post(registerUrl,data=registerData,headers=self.header,name=registerUrlName+registerUrl,verify=False,allow_redirects=False,catch_response=True) as registerResponse:
            if "200" in registerResponse:
                register_res = json.loads(registerResponse.text)
                if 'code' in register_res and register_res["code"] == 200:
                    # print("注册手机号是：{}".format(mobile))
                    # self.logger.get_locust_Hook() #重点！此处挂载Log日志钩子
                    registerResponse.success()
                elif 'code' in register_res and register_res["code"] == 438:
                    print("手机号{}已存在".format(mobile))
                    registerResponse.failure("手机号{}已存在".format(mobile))
                elif 'code' in register_res and register_res["code"] == 437:
                    # print("验证码失效,请从新发送=====手机号是：{}短信验证码是------{}".format(mobile,code))
                    registerResponse.failure("验证码失效,请从新发送=====手机号是：{}".format(mobile))
                else:
                    print("手机号{}注册失败{}".format(str(mobile),register_res))
                    registerResponse.failure("手机号{}注册失败{}".format(str(mobile),register_res))
            else:
                registerResponse.failure("手机号{}注册失败{}".format(str(mobile),registerResponse))

    # @task(1)   
    def userLogin(self):
        """
        登录
        """
        self.ZhuCeMa()
        try:
            userItem = self.user.queueData.get()  #获取队列里的数据
            # print("登录用户：",userItem)
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        print("shoujihao ====== {}".format(userItem['mobile']))
        login_urlName = "登录"
        login_url = "/gateway/member/login"
        login_data = {
                "gid": "866215038845167",
                "code": "1234",
                "logintype": 0,
                "mobile": userItem['mobile'],
                "pass": "c80d171b81624145618791d99107554a",
                "channel": 2
            }
        self.loginRes = PublicRequest(self).publicRequest(login_url, login_urlName, login_data, self.header)
        print("-------------------------",self.loginRes)
        if self.loginRes:
            self.header["token"] = self.loginRes["data"]["token"]
            self.loginRes['header'] = self.header
            '''
            判断用户初始化信息是否完善，不完善则先完善
            '''
            # if "遍地开花" in self.loginRes["data"]["nickname"]:
            #     print("修改头像")
            if self.loginRes["data"]['status'] == 0:
                self.initializeUser(self.loginRes["data"],self.header)
            return self.loginRes


    def initializeUser(self,loginUser,header):
        '''
        初始化用户信息
        '''
        sex = random.randint(1,2)
        nickname = u'遍地开花'+str(loginUser['uid'])
        year = random.randint(1919,2007)
        month = random.randint(1,12)
        day = ''
        if month == 2:
            day = random.randint(1,28) 
        else:
            day = random.randint(1,30)
        strmonth = self.zhuanHuan(month)
        strdat = self.zhuanHuan(day)
        birthday = str(year)+strmonth+strdat
        tp1 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/b15d68032039ac4760d441a354d63915.png"
        tp2 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/e054a045cf326473a7835cb02778ca74.png"
        tp3 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/fbff95e3bcf343629cfbb7235e4fde69.png"
        tp4 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/884841df03eb73efdfa9ef1d0f91e3e6.png?rnd=5"
        tp5 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/97dc4501edd919ef819631cf00e6ea63.png"
        tp6 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/4bdb7c17833b882bf19dbe0e3c72d883.png?range=640640"
        tp7 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/bbb984142aa931be126de06cdbfba3a8.png?rnd=1"
        tp8 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/3b7241170fa261a513bb9ac00b0d9bea.png"
        tp9 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/2a6b2ddbdd4bfcdb88347291beee7036.png"
        tp9 = "https://youtime-test.oss-cn-beijing.aliyuncs.com/3b7241170fa261a513bb9ac00b0d9bea.png?rnd=11"
        picture = [tp1,tp2,tp3,tp4,tp5,tp6,tp7,tp8,tp9]
        avatar = random.choice(picture)
        cs_data = {
            "sex": sex,
            "nickname": nickname,
            "birth": birthday,
            "avatar": avatar
        }
        cs_url = "/gateway/member/editinfo"
        cs_urlName = "初始化用户信息"
        return PublicRequest(self).publicRequest(cs_url, cs_urlName, cs_data, header)


    def zhuanHuan(self,number):
        if number>9:
            return str(number)
        else:
            return "0"+str(number)


    def ZhuCeMa(self):
        """
        # 注册码
        """
        # 将verify 设置为 False，Requests 将忽略对 SSL 证书的验证
        header = {"Connection":"keep-alive"}
        zcm_urlName = "注册码"
        zcm_url = "/gateway/member/macregister"
        zcm_data = {
            "qudao": "1",
            "gid": int(time.time()), #设备唯一标识
            "clientid": "e34f1fa5127db91fdda825528c57c9ad8",
            "os": "9",
            "machine": "V1829A",
            "version": "1.0",
            "platform": "android"
        }
        zcm_response = PublicRequest(self).requestMethod(zcm_url,zcm_urlName,zcm_data,header)
        if zcm_response.status_code == 200:
            zcm_res = json.loads(zcm_response.text)
            token = zcm_res['data']['token']
            num = int(time.time())
            self.header = {
                "token":token,
                "time":str(num),
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent":"okhttp/2.7.5",
                "Connection": "keep-alive",
                "Accept-Encoding":"gzip"
            }
            # zcm_response.success()
        else:
            print("XXX生成注册码失败XXX===={}".format(zcm_response.status_code))
            zcm_response.failure("XXX生成注册码失败XXX===={}".format(zcm_response.status_code))

    
    


