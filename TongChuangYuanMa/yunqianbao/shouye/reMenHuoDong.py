from locust import TaskSet
import time,json,random,sys
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from yunqianbao.qianMing import GetDataSign




class ReMenHuoDong(TaskSet):

    def recruitingRepresentatives(self,apikey,header,login_res):
        """"
        招募股东代表(申请状态)
        """
        hdlist_url = "v2/shareholders/recruit"
        hdlist_urlName = "招募股东代表"
        hdlist_data = {
            "access_token":login_res["access_token"],
            "sign":"",
            "timestamp":str(int(time.time()))
        }
        sign = GetDataSign().sign_body(hdlist_url,hdlist_data, apikey)
        hdlist_data["sign"] = sign
        with self.client.post(hdlist_url,data = hdlist_data, headers = header,name = hdlist_urlName+hdlist_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                zmdb_res = json.loads(response.text)
                if "status" in zmdb_res and zmdb_res["status"] == 200:
                    response.success()
                    return zmdb_res["data"]
                else:
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(hdlist_urlName,hdlist_url,hdlist_data,zmdb_res))
            else:
                response.failure("服务器响应错误==={}=={}".format(response,response.text))


    # def recruitingRepresentatives(self,apikey,header,login_res):
    #     """"
    #     申请成为股东代表
    #     """
    #     hdlist_url = "v2/user/card-status"
    #     hdlist_urlName = "申请成为股东代表"
    #     hdlist_data = {
    #         "access_token":login_res["access_token"],
    #         "sign":"",
    #         "timestamp":str(int(time.time()))
    #     }
    #     sign = GetDataSign().sign_body(hdlist_url,hdlist_data, apikey)
    #     hdlist_data["sign"] = sign
    #     with self.client.post(hdlist_url,data = hdlist_data, headers = header,name = hdlist_urlName+hdlist_url,verify = False,allow_redirects=False,catch_response=True) as response:
    #         if "200" in str(response):
    #             zmdb_res = json.loads(response.text)
    #             if "status" in zmdb_res and zmdb_res["status"] == 200:
    #                 response.success()
    #                 return zmdb_res
    #             else:
    #                 response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(hdlist_urlName,hdlist_url,hdlist_data,zmdb_res))
    #         else:
    #             response.failure("服务器响应错误==={}=={}".format(response,response.text))


    def submitApplication(self,apikey,header,login_res):
        """"
        提交申请
        """
        tjsq_url = "/v2/shareholders/apply"
        tjsq_urlName = "提交申请"
        detail = """
        
            1、 测试目标：对测试目标进行简要的描述。

            2、 测试概要：摘要说明所需测试的软件、名词解释、以及提及所参考的相关文档。
            1、 测试目标：对测试目标进行简要的描述。

            2、 测试概要：摘要说明所需测试的软件、名词解释、以及提及所参考的相关文档。
            1、 测试目标：对测试目标进行简要的描述。

            2、 测试概要：摘要说明所需测试的软件、名词解释、以及提及所参考的相关文档。
            1、 测试目标：对测试目标进行简要的描述。

            2、 测试概要：摘要说明所需测试的软件、名词解释、以及提及所参考的相关文档。
        """
        tjsq_data = {
            "access_token":login_res["access_token"],
            "detail":detail,
            "sign":"",
            "timestamp":str(int(time.time())),
            "title":"团结就是力量"
        }
        sign = GetDataSign().sign_body(tjsq_url,tjsq_data, apikey)
        tjsq_data["sign"] = sign
        with self.client.post(tjsq_url,data = tjsq_data, headers = header,name = tjsq_urlName+tjsq_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                zmdb_res = json.loads(response.text)
                if "status" in zmdb_res and zmdb_res["status"] == 200:
                    response.success()
                    return zmdb_res
                else:
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(tjsq_urlName,tjsq_url,tjsq_data,zmdb_res))
            else:
                response.failure("服务器响应错误==={}=={}".format(response,response.text))




    def ReSubmitApplication(self,apikey,header,login_res,applyId):
        """"
        重新提交申请
        """
        tjsq_url = "/v2/shareholders/reapply"
        tjsq_urlName = "提交申请"
        detail = """这里开始kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk,kkkkk.kkkkkkk:'/kkkkk，kkkkk。！kkkkkkkk kkkkkkkkkkkkkkkkkkkkkkkkkkkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq!qqqqqqqqqqqqqqqqqqqqqqqqqqq这里终止"""
        tjsq_data = {
            "access_token":login_res["access_token"],
            "applyId":applyId,
            "detail":detail,
            "sign":"",
            "timestamp":str(int(time.time())),
            "title":"团结就是力量22222"
        }
        sign = GetDataSign().sign_body(tjsq_url,tjsq_data, apikey)
        tjsq_data["sign"] = sign
        with self.client.post(tjsq_url,data = tjsq_data, headers = header,name = tjsq_urlName+tjsq_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                zmdb_res = json.loads(response.text)
                if "status" in zmdb_res and zmdb_res["status"] == 200:
                    response.success()
                    return zmdb_res
                else:
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(tjsq_urlName,tjsq_url,tjsq_data,zmdb_res))
            else:
                response.failure("服务器响应错误==={}=={}".format(response,response.text))