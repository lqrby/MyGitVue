
from requests_toolbelt import MultipartEncoder
from locust import HttpUser,task,TaskSet,between
import sys, datetime, json, time, random, re


class LocustRequestUtil(TaskSet):

    
    def requestMethod(self,case, url, urlName, method, param=None, headers=None, content_type=None):
        """
        通用请求工具类
        """
        try:
            print("requestMethod")
            if method == "get":
                with self.client.get(url, name=urlName+url, params = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                    if "200" in str(response):
                        response.encoding = "utf-8"
                        assert_msg = self.assertResponse(case,response.text)
                        if assert_msg.get("is_pass") == True:
                            response.success()
                            return response.text
                        else:
                            response.failure("get断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                            print("get断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                            return False
                    else:
                        response.failure("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                        print("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                        return False
            elif method == "post":
                if content_type == "application/x-www-form-urlencoded":
                    print("content_type=============================================================================================================",content_type)
                    with self.client.post(url, data = param, headers=headers, name=urlName+url, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            assert_msg = self.assertResponse(case,response.text)
                            if assert_msg.get("is_pass") == True:
                                response.success()
                                return response.text
                            else:
                                response.failure("x-www-form断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                print("x-www-form断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                return False
                        else:
                            response.failure("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            print("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            return False

                elif content_type == "application/json":
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            assert_msg = self.assertResponse(case,response.text)
                            if assert_msg.get("is_pass") == True:
                                response.success()
                                return response.text
                            else:
                                response.failure("json断言失败url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response.text))
                                print("json断言失败--url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response.text))
                                return False
                        else:
                            response.failure("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            print("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            return False

                elif content_type == "multipart/form-data":
                    m = MultipartEncoder(param)
                    headers['Content-Type'] = m.content_type
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            assert_msg = self.assertResponse(case,response.text)
                            if assert_msg.get("is_pass") == True:
                                response.success()
                                return response.text
                            else:
                                response.failure("form-data断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                print("form-data断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                return False
                        else:
                            response.failure("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            print("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            return False

                else:
                    with self.client.post(url, name=urlName+url, data = param, headers=headers, verify=False, allow_redirects=False, catch_response=True) as response:
                        if "200" in str(response):
                            response.encoding = "utf-8"
                            assert_msg = self.assertResponse(case,response.text)
                            if assert_msg.get("is_pass") == True:
                                response.success()
                                return response.text
                            else:
                                response.failure("断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                print("断言失败:用例id={}--url={}--接口名称={}--响应码={}".format(case["id"], case["url"], case["title"]+case["url"], response.text))
                                return False
                        else:
                            response.failure("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            print("服务器状态码错误：用例id={},url={},接口名称={},响应码={}".format(case["id"], url,urlName,response))
                            return False
                    
                        
            else:
                print("http method not allowed")

        except Exception as e:
            print("压测http请求报错:{0}".format(e))

    


    def assertResponse(self,case,response):
        """
        断言响应内容，更新用例执行情况
        """

        is_pass = False
        response = json.loads(response)
        if not response:
            is_pass = True
            msg = '模块:{0}, 标题:{1}, 该接口未执行原因:{2}, 前置用例响应值:{3}'.format(case.get("module"), case.get("title"), "前置用例返回值无数据", response)
            assert_msg = {'is_pass':is_pass,'msg':msg}
            return assert_msg
        assert_type = case["assert_type"]
        print("1111111111111111111111",response)
        expect_result = json.loads(case["expect_result"])
        res_data = response.get("data")
        mark = False
        expect_result = json.loads(case["expect_result"])
        for code in expect_result: #判断业务状态码
            if code == response.get("status") or str(code) == response.get("status"):
                mark = True
                is_pass = True
                break
        if mark and res_data:
            if assert_type == "status":
                if res_data.get("token"):
                    self.token = res_data.get("token")
                is_pass = True
                print("测试用例通过1")
                # 判断列表数组长度
            elif assert_type == "data_list":
                data_array = res_data.get("list")
                if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
                    is_pass = True
                    print("测试用例通过2")
                else:
                    is_pass = False
                    print("测试用例不通过data-list")
            elif assert_type == "data_array":
                if res_data is not None and len(res_data) >= 0:
                    is_pass = True
                    print("测试用例通过3")
                else:
                    is_pass = False
                    print("测试用例不通过data_array")
            elif assert_type == "data_json":
                if res_data is not None and isinstance(res_data, dict) and len(res_data) > int(expect_result):
                    is_pass = True
                    print("测试用例通过4")
                else:
                    is_pass = False
                    print("测试用例不通过data_json")
            elif assert_type == "data_item":
                data_array = res_data.get("item")
                if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
                    is_pass = True
                    print("测试用例通过5")
                else:
                    is_pass = False
                    print("测试用例不通过data-item")
            else:
                print("测试用例data类型错误")
                is_pass = False
        msg = '模块:{0}, 标题:{1}, 断言类型:{2}, 响应:{3}'.format(case.get("module"), case.get("title"), assert_type, response)
        #拼装信息
        assert_msg = {'is_pass':is_pass,'msg':msg}
        return assert_msg
