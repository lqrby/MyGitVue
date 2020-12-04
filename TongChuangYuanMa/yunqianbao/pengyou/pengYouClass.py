from locust import TaskSet
import random,time,json
import base64
import sys
import queue
from requests_toolbelt import MultipartEncoder
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign
from yunqianbao.publicRequestMethod import PublicRequest
from yunqianbao.single.publicData import PublicDataClass
# from common.writeAndReadText import WriteAndReadTextFile



class PengYouClass(TaskSet):

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
        login_data = {
            "password":password,
            "latitude":"39.905662",
            "mobile":str(mobile),
            "long":"116.64063",
            "device_tokens":str(device_tokens),
            "timestamp":str(int(time.time())),
            "sign":	"" 
        }
        login_url = "v2/login/login2"
        sign = GetDataSign().sign_body(login_url,login_data, apikey)
        login_data["sign"] = sign
        
        #登录
        with self.client.post(login_url, data = login_data, headers = header, verify = False, allow_redirects=False,catch_response=True) as loginres:
            print("登录===={}".format(loginres.elapsed.total_seconds()))
            # print("loginres===",loginres)
            if "[200]" in str(loginres):
                loginresult = json.loads(loginres.text)
                if 'status' in loginresult and loginresult["status"] == 200 or 'status' in loginresult and loginresult["status"] == "200":
                    time.sleep(random.randint(1,3))
                    login_res = loginresult["data"]
                    print("登录成功啦")
                    loginres.success()
                    return login_res
                elif 'status' in loginresult and loginresult["status"] == 421:
                    print("登录成功啦啊啦啦啦啦啦啦")
                    loginres.success()
                    time.sleep(random.randint(1,3))
                    login_res = PublicDataClass(self).miBaoWenTi(apikey,header)
                    return login_res
                elif 'status' in loginresult and loginresult["status"] == 412:
                    print("请打开应用权限") #应用管理》进入app权限设置》应用权限》设置单项权限》获取手机识别码
                    loginres.failure("{}XXX===={}".format(str(mobile),password))   
                elif 'status' in loginresult and loginresult["status"] == 1006:
                    print("用户名或密码错误")
                    loginres.failure("{}XXX===={}".format(str(mobile),password))    
                else:
                    print("报错url==={} ，参数==={} ，报错原因==={}".format(login_url,login_data,loginresult))
                    loginres.failure("报错url==={} ，参数==={} ，报错原因==={}".format(login_url,login_data,loginresult))
            else:
                print("XXXXX登录出现意想不到的错误XXXXX")
                loginres.failure("登录出现意想不到的错误报错url==={} ，参数==={} ，报错原因==={}".format(login_url,login_data,loginres.text))

    def pengYou(self,apikey,header,login_res):
        """
        进入朋友模块》聊天记录列表
        """
        pylist_url = "/v2/group/my-group-list"              
        pylist_urlName = "朋友模块列表"  
        pylist_data = {
            "access_token":login_res["access_token"],
            "page":1,
            "sign":"",
            "timestamp":str(int(time.time())),
            "type":3
        }
        sign = GetDataSign().sign_body(pylist_url,pylist_data, apikey)
        pylist_data["sign"] = sign
        pylist_respons = PublicRequest(self).publicRequest(pylist_url,pylist_urlName,pylist_data,header)
        if pylist_respons:
            return pylist_respons["data"]["list"]


    def getInfo(self,apikey,header,login_res,group_id):
        """
        进入朋友或群的聊天页
        return 群成员list
        """
        infolist_url = "/v2/group/member-list"              
        infolist_urlName = "进入朋友或群的聊天页"  
        infolist_data = {
            "access_token":login_res["access_token"],
            "group_id":group_id,
            "sign":"",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(infolist_url,infolist_data, apikey)
        infolist_data["sign"] = sign
        infolist_respons = PublicRequest(self).publicRequest(infolist_url,infolist_urlName,infolist_data,header)
        if infolist_respons:
            return infolist_respons["data"]
    
    def hairRedEnvelopes(self,apikey,header,login_res,group_id):
        """
        发红包
        """
        hair_url = "/v2/gift/give"              
        hair_urlName = "发红包"  
        aics = random.randint(1,50)
        hair_data = {
            "access_token":login_res["access_token"],
            "pay_pwd":"e10adc3949ba59abbe56e057f20f883e",
            "group_id":group_id,
            "aics":str(aics),
            "title":"恭喜发财,大吉大利",
            "nums":str(random.randint(1,aics)),
            "timestamp":str(int(time.time())),
            "sign":""
        }
        sign = GetDataSign().sign_body(hair_url,hair_data, apikey)
        hair_data["sign"] = sign
        hair_respons = PublicRequest(self).publicRequest(hair_url,hair_urlName,hair_data,header)
        if hair_respons and hair_respons["status"] == 200:
            print("发红包成功，红包id是：{}".format(hair_respons["data"]["gift_id"]))
            return hair_respons["data"]["gift_id"]

    def robRedEnvelopes(self,apikey,header,login_res,gift_id):
        """
        抢红包
        """
        roblist_url = "/v2/gift/giftinfo"              
        roblist_urlName = "抢红包"  
        roblist_data = {
            "access_token":login_res["access_token"],
            "gift_id":gift_id,
            "sign":"",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(roblist_url,roblist_data, apikey)
        roblist_data["sign"] = sign
        roblist_respons = PublicRequest(self).publicRequest(roblist_url,roblist_urlName,roblist_data,header)
        if roblist_respons:
            return roblist_respons["data"]["info"]

                 
    def openRedEnvelopes(self,apikey,header,login_res,gift_id,group_id):
        """
        打开红包
        """
        openlist_url = "/v2/gift/receive"              
        openlist_urlName = "打开红包"  
        openlist_data = {
            "access_token":login_res["access_token"],
            "gift_id":gift_id,
            "group_id":group_id,
            "sign":"",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(openlist_url,openlist_data, apikey)
        openlist_data["sign"] = sign
        openlist_respons = PublicRequest(self).publicRequest(openlist_url,openlist_urlName,openlist_data,header)
        return openlist_respons


    def friendsInGroups(self):
        "拉好友入群"
        pass


    def addFriends(self,apikey,header,login_res,mobile):
        """"
        查找好友uid
        """
        czhyurl = "/v2/friends/open-user"
        czhyurlName = "查找好友"
        czhyData = {
            "access_token":	login_res["access_token"],
            "sign":"",
            "timestamp":str(int(time.time())),
            "username":str(mobile)
        }
        sign = GetDataSign().sign_body(czhyurl,czhyData, apikey)
        czhyData["sign"] = sign
        czhylist_respons = PublicRequest(self).publicRequest(czhyurl,czhyurlName,czhyData,header)
        if czhylist_respons:
            return czhylist_respons["data"]["uid"]

    def getUserDetail(self,apikey,header,login_res,uid):
        """"
        根据uid查看用户详情
        """
        xq_url = "/v2/friends/id-user"
        xq_urlName = "根据uid查看用户详情"
        xq_data = {
            "access_token":	login_res["access_token"],
            "sign":"",
            "timestamp":str(int(time.time())),
            "username":uid
        }
        sign = GetDataSign().sign_body(xq_url,xq_data, apikey)
        xq_data["sign"] = sign
        xqlist_respons = PublicRequest(self).publicRequest(xq_url,xq_urlName,xq_data,header)
        if xqlist_respons:
            return xqlist_respons["data"]


    # def getUserDetail(self,apikey,header,login_res,uid):
    #     """"
    #     根据uid添加对方为好友
    #     """
    #     tjhy_url = "/v2/friends-apply/applyfor"
    #     tjhy_urlName = "根据uid添加对方为好友"
    #     tjhy_data = {
    #         "access_token":	login_res["access_token"],
    #         "message":"你好",
    #         "sign":"",
    #         "timestamp":str(int(time.time())),
    #         "uid":uid
    #     }
    #     sign = GetDataSign().sign_body(tjhy_url,tjhy_data, apikey)
    #     tjhy_data["sign"] = sign
    #     tjhylist_respons = PublicRequest(self).publicRequest(tjhy_url,tjhy_urlName,tjhy_data,header)
    #     # print("tjhylist_respons====",tjhylist_respons)
    #     if tjhylist_respons:
    #         return tjhylist_respons["status"]




    def message(self,apikey,header,login_res):
        xxurl = "/v2/friends-apply/list"
        xxurlName = "好友请求待验证列表"
        xxdata = {
            "access_token":login_res["access_token"],
            "page":"1",
            "sign":"",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(xxurl,xxdata,apikey)
        xxdata["sign"] = sign
        tjhylist_respons = PublicRequest(self).publicRequest(xxurl,xxurlName,xxdata,header)
        if tjhylist_respons:
            return tjhylist_respons["data"]["list"]

    def passValidation(self,apikey,header,login_res,id):
        """
        通过添加好友的验证
        """
        tgyz_url = "/v2/friends-apply/set-friend"
        tgyz_urlName = "通过添加好友的验证"
        tgyz_data = {
            "access_token":login_res["access_token"],
            "id":id,
            "sign":"",
            "status":"1",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(tgyz_url,tgyz_data,apikey)
        tgyz_data["sign"] = sign
        tgyzlist_respons = PublicRequest(self).publicRequest(tgyz_url,tgyz_urlName,tgyz_data,header)
        if tgyzlist_respons:
            return tgyzlist_respons["status"]
    


