
# import requests
from requests_toolbelt import MultipartEncoder
from locust import HttpUser,task,TaskSet,between
import sys,json,time,random
# sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression_2")
# from common.qianMing import GetDataSign


class LocustRequestUtil(TaskSet):

    # def __init__(self):
    #     pass

    def requestMethod(self, url, urlName, method, param=None, headers=None, content_type=None):
        """
        通用请求工具类
        """
        try:
            print("requestMethod")
            if method == "get":
                with self.client.get(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                    if "200" in str(response):
                        response.encoding = "utf-8"
                        return response
                    else:
                        response.failure("url:{}--接口名称:{}--响应码:{}".format(url,urlName,response))
                        print("状态码错误：{}".format(response))

            elif method == "post":
                if content_type == "application/x-www-form-urlencoded":
                    with self.client.post(url, data = param, headers=headers, name=urlName+url, verify=False, allow_redirects=False, catch_response=True) as response:
                        print("响应结果======{}".format(response))
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            return response
                        else:
                            response.failure("url:{}--接口名称:{}--响应码:{}".format(url,urlName,response))
                            print("状态码错误：{}".format(response))

                elif content_type == "application/json":
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            return response
                        else:
                            response.failure("url:{}--接口名称:{}--响应码:{}".format(url,urlName,response))
                            print("状态码错误：{}".format(response))

                elif content_type == "multipart/form-data":
                    m = MultipartEncoder(param)
                    headers['Content-Type'] = m.content_type
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            return response
                        else:
                            response.failure("url:{}--接口名称:{}--响应码:{}".format(url,urlName,response))
                            print("状态码错误：{}".format(response))

                else:
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            return response
                        else:
                            response.failure("url:{}--接口名称:{}--响应码:{}".format(url,urlName,response))
                            print("状态码错误：{}".format(response))
                    
                        
            else:
                print("http method not allowed")

        except Exception as e:
            print("压测http请求报错:{0}".format(e))
