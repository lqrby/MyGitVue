import time, requests, json
from locust import TaskSet
import sys, queue, re
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_performance")
from common.qianMing import GetDataSign
from common.publicRequestMethod import PublicRequest
from common.publicData import PublicDataClass
class LingGuXi(TaskSet):
    

    def getGassport(self,loginUser,apikey,header):  #goToLingShuiDi

        qlgx_url = "v2/activity/aic-tree-entrance"
        qlgx_urlName = "去领股息--获取passport"
        qlgx_data = {
            "access_token":loginUser["access_token"],
            "timestamp":str(int(time.time() * 100000)),
            "sign":"" 
        }
        sign = GetDataSign().sign_body(qlgx_url, qlgx_data, apikey)
        qlgx_data["sign"] = sign
        qlgx_respons = PublicRequest(self).publicRequest(qlgx_url,qlgx_urlName,qlgx_data,header)
        if qlgx_respons and qlgx_respons.get("status") and qlgx_respons.get("status") == 200:
            url = qlgx_respons["data"]["url"]
            passport = re.search("passport=(.*)", str(url)).group(1)
            return passport

    def waterList(self,passport,h5_header): 
        '''
        领取水滴列表
        '''
        print("领取水滴列表")
        lqsdList_url = "mapi/aic-tree/mission-status"
        lqsdList_urlName = "领取水滴列表"
        lqsdList_data = {
            "passport":passport
        }
        with self.client.get(url = lqsdList_url,params=lqsdList_data,name=lqsdList_urlName+lqsdList_url,headers=h5_header,verify=False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                lqsdList_res = json.loads(response.text)
                if lqsdList_res.get("status") and lqsdList_res.get("status") == 200:
                    sd_list = []
                    for item in lqsdList_res["data"]:
                        if item.get("status") == 1:
                            sd_list.append(item)
                    response.success()
                    return sd_list
                else:
                    print("请求错误")
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(lqsdList_urlName,lqsdList_url,lqsdList_data,response))
            else:
                print("服务器请求错误")
                response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(lqsdList_urlName,lqsdList_url,lqsdList_data,response))


    def getWater(self,passport,item,h5_header):  
        '''
        领取水滴
        '''
        print("领取水滴")
        lqsd_urlName = "领取水滴"
        lqsd_url = "mapi/aic-tree/get-water"
        lqsd_data = {
            "passport":passport,
            "type":item["type"]
        }
        with self.client.get(url = lqsd_url,params=lqsd_data,name=lqsd_urlName+lqsd_url,headers=h5_header,verify=False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                lqsd_res = json.loads(response.text)
                print("9999======",lqsd_res)
                if lqsd_res.get("status") and lqsd_res.get("status") == 200:
                    response.success()
                    return lqsd_res["data"]
                else:
                    print("领取水滴请求错误")
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(lqsd_urlName,lqsd_url,lqsd_data,response.text))
            else:
                print("领取水滴服务器请求错误")
                response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(lqsd_urlName,lqsd_url,lqsd_data,response))
       
       
        

