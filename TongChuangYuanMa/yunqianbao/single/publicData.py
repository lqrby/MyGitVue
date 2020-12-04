from locust import TaskSet
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from common.writeAndReadText import WriteAndReadTextFile

class PublicDataClass(TaskSet):
    
    def zhuceUser(self,apikey,header):
        try:
            mobile = self.user.queueData.get()  #获取队列里的数据
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        devicetokens = int(round(time.time() * 1000)) #"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN"
        zc_data = {
            # "password":"defe12aad396f90e6b179c239de260d4", #123456ab
            "password":"c80d171b81624145618791d99107554a", #ren123456
            "latitude":"39.905662",
            "mobile":str(mobile),
            "long":"116.64063",
            "device_tokens":str(devicetokens),
            "timestamp":str(int(time.time())),
            "sign":	"" 
        }

        zc_url = "v2/login/signup"
        sign = GetDataSign().sign_body(zc_url,zc_data,apikey)
        zc_data["sign"] = sign
        zc_respons = PublicRequest(self).requestMethod(zc_url,zc_data,header)
        zcres = json.loads(zc_respons.text)
        if 'status' in zcres and zcres["status"] == 200 or zcres["status"] == "200":
            zc_respons.success()
            print("注册用户成功===={}".format(mobile))
            return zcres["data"]
        elif 'status' in zcres and zcres["status"] == 422 or zcres["status"] == "422":
            print("此手机号已注册==={}".format(str(mobile)))
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(zc_url,zc_data,zcres))
            zc_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(zc_url,zc_data,zcres))


    def userLogout(self,apikey,header,login_res):
        logout_url = "v2/login/logout"
        logout_urlName = "用户退出"
        logout_data = {
            "access_token":login_res["access_token"],
            "timestamp":str(int(time.time())),
            "sign":""
        }
        sign = GetDataSign().sign_body(logout_url,logout_data,apikey)
        logout_data["sign"] = sign
        return PublicRequest(self).publicRequest(logout_url,logout_urlName,logout_data,header)


    def login(self,apikey,header):
        """"
        登录》获取首页》判断密保(未设置密保先设置密保)》判断是否实名(未实名则先实名)
        
        """
        try:
            mobile = self.user.queueData.get()  #获取队列里的数据
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        password = "c80d171b81624145618791d99107554a" #
        device_tokens = int(round(time.time() * 1000)) #"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN"
        self.login_data = {
            "password":"c80d171b81624145618791d99107554a",
            "latitude":"39.905662",
            "mobile":"18810798467",
            "long":"116.64063",
            "device_tokens":"",
            "timestamp":str(int(time.time())),
            "sign":	"" 
        }
        login_url = "v2/login/login2"
        sign = GetDataSign().sign_body(login_url,self.login_data, apikey)
        print("sign====",sign)
        self.login_data["sign"] = sign
        
        #登录
        loginres = PublicRequest(self).requestMethod(login_url,self.login_data,header)
        print("登录===={}".format(loginres.elapsed.total_seconds()))
        loginresult = json.loads(loginres.text)
        if 'status' in loginresult and loginresult["status"] == 200 or 'status' in loginresult and loginresult["status"] == "200":
            time.sleep(random.randint(1,3))
            login_res = loginresult["data"]
            loginres.success()
            return login_res
        elif 'status' in loginresult and loginresult["status"] == 421: #登录设备发生改变
            # loginres.success()
            time.sleep(random.randint(1,3))
            login_res = self.miBaoWenTi(apikey,header)
            return login_res
        elif 'status' in loginresult and loginresult["status"] == 412:
            print("请打开应用权限")
            loginres.failure("{}XXX===={}".format(str(mobile),password))   
        elif 'status' in loginresult and loginresult["status"] == 1006:
            print("用户名或密码错误")
            loginres.failure("{}XXX===={}".format(str(mobile),password))    
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(login_url,self.login_data,loginresult))
            loginres.failure("报错url==={} ，参数==={} ，报错原因==={}".format(login_url,self.login_data,loginresult))
        

    
    def miBaoWenTi(self,apikey,header):
        """
        # 登录设备发生改变，回答密保问题
        """
        daan_url = "v2/safe/answer"
        daan_data ={
            "password":self.login_data["password"],
            "question":"1",
            "answer":"北京",
            "latitude":self.login_data["latitude"],
            "mobile":self.login_data["mobile"],
            "long":	self.login_data["long"],
            "device_tokens":self.login_data["device_tokens"],
            "timestamp":self.login_data["timestamp"],
            "sign":	""
        }

        # 获取首页
        daan_data["sign"] = GetDataSign().sign_body(daan_url,daan_data, apikey)
        daan_respons = PublicRequest(self).requestMethod(daan_url,daan_data,header)
        daanres = json.loads(daan_respons.text)
        if 'status' in daanres and daanres["status"] == 200:
            time.sleep(random.randint(1,3))
            daan_respons.success()
            return daanres["data"]
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(daan_url,daan_data,daanres))
            daan_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(daan_url,daan_data,daanres))






    # @task(1)
    def index(self,apikey,header,login_res):
        # 获取首页的参数
        if login_res:
            index_url = "v2/my/index"
            index_data ={
                "access_token":login_res["access_token"],
                "sign":"",
                "timestamp":str(int(time.time()))
            }
            # 获取首页
            index_data["sign"] = GetDataSign().sign_body(index_url,index_data, apikey)
            sy_respons = PublicRequest(self).requestMethod(index_url,index_data,header)
            syres = json.loads(sy_respons.text)
            if 'status' in syres and syres["status"] == 200 or 'status' in syres and syres["status"] == "200":
                time.sleep(random.randint(1,3))
                sy_respons.success()
                return syres
            else:
                print("报错url==={} ，参数==={} ，报错原因==={}".format(index_url,index_data,syres))
                sy_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(index_url,index_data,syres))

   
   
    def setMiBao(self,apikey,header,login_res,is_safe):
        # 设置密保
        print("is_safe[data]==={}".format(is_safe))
        if is_safe["data"]["is_safe"] == "0":
            mibao_url = "v2/safe/set-safe-issue"
            mibao_data = {
                "access_token":login_res["access_token"],
                "answer":"W3siYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMCIsImlzc3VlIjoiMSJ9LHsiYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMCIsImlzc3VlIjoiMyJ9LHsiYW5zd2VyIjoi5YyX5LqsIiwiaXNfc3lzIjoiMSIsImlzc3VlIjoi5YyX5LqsIn1d",
                "timestamp":str(int(time.time())),
                "sign":""
            }
            # 提交设置的密保
            mibao_data["sign"] = GetDataSign().sign_body(mibao_url,mibao_data, apikey)
            mibao_respons = PublicRequest(self).requestMethod(mibao_url,mibao_data,header)
            mibaores = json.loads(mibao_respons.text)
            if 'status' in mibaores and mibaores["status"] == 200 or 'status' in mibaores and mibaores["status"] == "200":
                time.sleep(random.randint(1,3))
                mibao_respons.success()
                return mibaores
            else:
                print("报错url==={} ，参数==={} ，报错原因==={}".format(mibao_url,mibao_data,mibaores))
                mibao_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(mibao_url,mibao_data,mibaores))


    def shiMing(self,apikey,header,login_res,sfz_path):
        # 实名认证
        if login_res["info"]["idcard"] == None:
            card = WriteAndReadTextFile().readAndRemoveOneLine(sfz_path)
            print("实名人员====={}".format(card))
            if card: 
                card_list = card.split(" ")
                shiming_url = "v2/card/user-real-name"
                fields = {
                    "access_token":login_res["access_token"],
                    "idcard":card_list[1], #身份证号码
                    "degree":"0",
                    "sign":"",
                    "realname":card_list[0], #用户姓名
                    "timestamp":str(int(time.time())),
                    "image_face":('tp1.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp1.jpg", "rb"),"multipart/form-data"), #脸部照片
                    "image_con":('tp2.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp2.jpg", "rb"),"multipart/form-data"), #背面照片
                    "image_hand":('tp3.jpg',open("F:/myTestFile/TestObject/YouTime/yunqianbao/img/tp3.jpg", "rb"),"multipart/form-data") #手持正面照片 
                }
                # # 实名
                sign = GetDataSign().sign_body(shiming_url,fields, apikey)
                fields["sign"] = sign
                m = MultipartEncoder(fields)
                header['Content-Type'] = m.content_type
                with self.client.post(shiming_url,data=m,headers=header,verify=False,allow_redirects=False,catch_response=True) as sm_respons:
                    if "[200]" in str(sm_respons):
                        smres = json.loads(sm_respons.text)
                        if 'status' in smres and smres["status"] == 200 or 'status' in smres and smres["status"] == "200":
                            time.sleep(random.randint(1,3))
                            sm_respons.success()
                            return smres
                        else:
                            print("报错url==={} ，参数==={} ，报错原因==={}".format(shiming_url,m,smres))
                            sm_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(shiming_url,m,sm_respons.text))
                    else:
                        print("XXXXX服务器报错XXXXX")
                        sm_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(shiming_url,m,sm_respons))
                header['Content-Type'] = "application/x-www-form-urlencoded"
            else:
                print("XXX没有实名的身份证号了XXX")
                # self.interrupt(reschedule=True)
        # else:
        #     print("zhi shi====={}".format(login_res["info"]))
        
    def getDangQiId(self,apikey,header,login_res):
        """"
        获取当期id
        """
        dq_url = "v2/new-year20/online-period"
        dq_data = {
            "access_token":login_res["access_token"],
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        dq_data["sign"] = GetDataSign().sign_body(dq_url,dq_data, apikey)
        jrhqy_respons = PublicRequest(self).requestMethod(dq_url,dq_data,header)
        dqres = json.loads(jrhqy_respons.text)
        if 'status' in dqres and dqres["status"] == 200 or 'status' in dqres and dqres["status"] == "200":
            time.sleep(random.randint(1,3))
            jrhqy_respons.success()
            return dqres["data"]
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(dq_url,dq_data,dqres))
            jrhqy_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(dq_url,dq_data,dqres))


    # @task(1)
    def comTask(self,apikey,header,login_res,dqid):
        """"
        进入申请任务页
        
        """
        jrhqy_url = "v2/new-year20/actindex"
        jrhqy_data = {
            "access_token":login_res["access_token"],
            "periodId": dqid,
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        jrhqy_data["sign"] = GetDataSign().sign_body(jrhqy_url,jrhqy_data, apikey)
        jrhqy_respons = PublicRequest(self).requestMethod(jrhqy_url,jrhqy_data,header)
        jrhqyres = json.loads(jrhqy_respons.text)
        if 'status' in jrhqyres and jrhqyres["status"] == 200 or 'status' in jrhqyres and jrhqyres["status"] == "200":
            time.sleep(random.randint(1,3))
            jrhqy_respons.success()
            return jrhqyres
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(jrhqy_url,jrhqy_data,jrhqyres))
            jrhqy_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(jrhqy_url,jrhqy_data,jrhqyres))


    def getUserType(self,apikey,header,login_res):
        """"
        获取实名认证的状态
        
        """
        rw_url = "v2/user/card-status"
        renwu_data = {
            "access_token":login_res["access_token"],
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(rw_url,renwu_data, apikey)
        renwu_data["sign"] = sign
        #进入获取任务页面请求
        sfzpath = "E:/myTestFile/TestObject/TongChuangYuanMa/yunqianbao/static/shenfenzheng.txt"
        renwu_respons = PublicRequest(self).requestMethod(rw_url,renwu_data,header)
        zfrwres = json.loads(renwu_respons.text)
        if 'status' in zfrwres and zfrwres["status"] == 200 or zfrwres["status"] == "200":
            time.sleep(random.randint(1,3))
            renwu_respons.success()
            taskdata = zfrwres["data"]["type"]
            if taskdata == 5:
                # print("{}用户状态==={}===已实名通过".format(login_res["mobile"],taskdata))
                return taskdata
            elif taskdata == 3:
                print("{}用户状态==={}===待审核".format(login_res["mobile"],taskdata))
            elif taskdata == 1:
                print("{}用户状态==={}===未实名,现在去提交审核资料".format(login_res["mobile"],taskdata))
                self.shiMing(apikey,header,login_res,sfzpath) #实名认证
                print("{}用户提交了审核资料=={}".format(login_res["mobile"],taskdata))
            elif taskdata == 2:
                print("{}用户状态=={}==未实名,现在去提交审核资料".format(login_res["mobile"],taskdata))
                self.shiMing(apikey,header,login_res,sfzpath) #实名认证
            else:
                print("{}用户状态=={}".format(login_res["mobile"],taskdata))

                
        elif 'status' in zfrwres and zfrwres["status"] == 401 or zfrwres["status"] == "401":
            print("未登录或已退出")
            # self.interrupt(reschedule=True)
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(rw_url,renwu_data,zfrwres))
            renwu_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(rw_url,renwu_data,zfrwres))
            
    # @task(100)
    def paymentTaskMoney(self,apikey,header,login_res):
        """"
        支付任务押金
        
        """
        # if self.selectGoldShares():
        zfrw_url = "v2/new-year20/receive"
        zfrw_data = {
            "access_token":login_res["access_token"],
            "payPwd":"e10adc3949ba59abbe56e057f20f883e", #123456
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(zfrw_url,zfrw_data, apikey)
        zfrw_data["sign"] = sign
        #支付任务押金
        zfrw_respons = PublicRequest(self).requestMethod(zfrw_url,zfrw_data,header)
        print("支付任务响应时间===={}".format(zfrw_respons.elapsed.total_seconds()))
        zfrwres = json.loads(zfrw_respons.text)
        if 'status' in zfrwres and zfrwres["status"] == 200:
            time.sleep(random.randint(1,3))
            zfrw_respons.success()
            return "200"
        elif 'status' in zfrwres and zfrwres["status"] == 425:
            print("金股小于7枚，无法参与活动")
        elif 'status' in zfrwres and zfrwres["status"] == 441:
            # 还没有设置支付密码
            return "441"
        elif 'status' in zfrwres and zfrwres["status"] == 440:
            print("当日任务已达到上限")
            # self.interrupt(reschedule=True)
            #当日任务已达到上限
            return "440"
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(zfrw_url,zfrw_data,zfrwres))
            zfrw_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(zfrw_url,zfrw_data,zfrwres))


    
    def selectGoldShares(self,apikey,header,login_res):
        """"
        查询金股余额
        
        """
        xzc_url = "v2/wallet/new-assets"
        xzc_data = {
            "access_token":login_res["access_token"],
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(xzc_url,xzc_data, apikey)
        xzc_data["sign"] = sign
        #获取资产
        xzc_respons = PublicRequest(self).requestMethod(xzc_url,xzc_data,header)
        xzsres = json.loads(xzc_respons.text)
        if 'status' in xzsres and xzsres["status"] == 200 or xzsres["status"] == "200":
            time.sleep(random.randint(1,3))
            xzc_respons.success()
            goldShares = xzsres["data"]
            thighs_int = int(goldShares["thighs"]) #金股数量
            usdt_int = int(goldShares["usdt"])  #aic数量
            print("金股数量===={},aic数量======{}".format(thighs_int,usdt_int))
            if thighs_int > 7:
                print("11111")
                return True
            xcsl = 7 - thighs_int 
            if int(usdt_int/1000) > xcsl:
                print("2222")
            # 把aic兑换成金股
                self.exchangeGoldShares(apikey,header,login_res,xcsl+1)
                return True
            else:
                print("====金股余额不足,并且aic余额也不足===={}".format(login_res))
                # self.interrupt(reschedule=True)
        


    def exchangeGoldShares(self,apikey,header,login_res,num):
        """"
        兑换金股
        
        """
        dhjg_url = "v2/thigh/exchange-more"
        dhjg_data = {
            "access_token":login_res["access_token"],
            "num":str(num), #兑换金股的数量
            "paypwd":"e10adc3949ba59abbe56e057f20f883e",
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(dhjg_url,dhjg_data, apikey)
        dhjg_data["sign"] = sign
        #先查询用户是否有交易密码

        #兑换金股
        dh_respons = PublicRequest(self).requestMethod(dhjg_url,dhjg_data,header)
        print("兑换金股===={}".format(dh_respons.elapsed.total_seconds()))
        dhres = json.loads(dh_respons.text)
        if 'status' in dhres and dhres["status"] == 200 or 'status' in dhres and dhres["status"] == "200":
            time.sleep(random.randint(1,3))
            dh_respons.success()
            return "200"
        elif 'status' in dhres and dhres["status"] == 402 or 'status' in dhres and dhres["status"] == "402":
            dh_respons.success()
            print("未设置密码")
            return "402"
            # if self.setPaymentPassword():
            #     print("已设置密码")
            #     dh_respons = PublicRequest(self).requestMethod(dhjg_url,dhjg_data,header)
            #     dhres = json.loads(dh_respons.text)
            #     if 'status' in dhres and dhres["status"] == 200 or 'status' in dhres and dhres["status"] == "200":
            #         time.sleep(random.randint(1,3))
            #         print("兑换金股成功")
            #         dh_respons.success()
            #         return dhres
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(dhjg_url,dhjg_data,dhres))
            dh_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(dhjg_url,dhjg_data,dhres))
       

    def queryPaymentPassword(self,apikey,header,login_res):
        """"
        查询用户是否设置了支付密码
        
        """
        cxzfmm_url = "v2/wallet/trade-wallet"
        cxzfmm_data = {
            "access_token":login_res["access_token"],
            "paypwd":"e10adc3949ba59abbe56e057f20f883e",
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        # print("设置密码data====={}")
        sign = GetDataSign().sign_body(cxzfmm_url,cxzfmm_data, apikey)
        cxzfmm_data["sign"] = sign
        # print("sigin ======= {}".format(setzfmm_data["sign"]))
        #设置交易密码
        cxzfmm_respons = PublicRequest(self).requestMethod(cxzfmm_url,cxzfmm_data,header)
        cxzfmmres = json.loads(cxzfmm_respons.text)
        # print("查询交易密码结果====={}".format(cxzfmmres))
        if 'status' in cxzfmmres and cxzfmmres["status"] == 200 or 'status' in cxzfmmres and cxzfmmres["status"] == "200":
            time.sleep(random.randint(1,3))
            cxzfmm_respons.success()
            return cxzfmmres["data"]["userWallet"]
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(cxzfmm_url,cxzfmm_data,cxzfmmres))
            cxzfmm_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(cxzfmm_url,cxzfmm_data,cxzfmmres))
       

    def setPaymentPassword(self,apikey,header,login_res):
        """"
        设置支付密码
        
        """
        setzfmm_url = "v2/wallet/set-paypwd"
        setzfmm_data = {
            "access_token":login_res["access_token"],
            "password":"e10adc3949ba59abbe56e057f20f883e",
            "timestamp":str(int(time.time())),
            "sign":	""
        }
        sign = GetDataSign().sign_body(setzfmm_url,setzfmm_data, apikey)
        setzfmm_data["sign"] = sign
        #设置交易密码
        setzfmm_respons = PublicRequest(self).requestMethod(setzfmm_url,setzfmm_data,header)
        print("设置密码===={}".format(setzfmm_respons.elapsed.total_seconds()))
        setzfmmres = json.loads(setzfmm_respons.text)
        print("设置交易密码结果====={}".format(setzfmmres))
        if 'status' in setzfmmres and setzfmmres["status"] == 200 or 'status' in setzfmmres and setzfmmres["status"] == "200":
            time.sleep(random.randint(1,3))
            setzfmm_respons.success()
            return setzfmmres
        else:
            print("报错url==={} ，参数==={} ，报错原因==={}".format(setzfmm_url,setzfmm_data,setzfmmres))
            setzfmm_respons.failure("报错url==={} ，参数==={} ，报错原因==={}".format(setzfmm_url,setzfmm_data,setzfmmres))
