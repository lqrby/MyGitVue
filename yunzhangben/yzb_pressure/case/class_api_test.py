import sys, datetime, json, time, random, re, queue
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_pressure")
from utils.db_util import MysqlDb
from utils.locust_request_util import LocustRequestUtil
from utils.send_mail import SendMail
from case.qianMing import GetDataSign
from locust import HttpUser,task,TaskSet,between,events


class ZFAclassTestCase(TaskSet):

    
    def loadAllClassByApp(self,app_name_id):
        """
        根据app加载全部用例
        """
        print("loadAllClassByApp")
        my_db = MysqlDb()
        sql = "select * from `testcaseapp_case` where app_name_id = '{0}'".format(app_name_id)
        results = my_db.query(sql)
        return results


    def findCaseById(self,case_id):
        """
        根据id找测试用例
        """
        print("findCaseById")
        my_db = MysqlDb()
        sql = "select * from `testcaseapp_case` where id = '{0}'".format(case_id)
        returns = my_db.query(sql, state="one")
        return returns


    def loadConfigByAppAndKey(self,app_name,dict_key):
        """
        根据app和key加载配置
        """
        print("loadConfigByAppAndKey")
        my_db = MysqlDb()
        sql = "select * from `testcaseapp_config` where name='{0}' and dict_key='{1}'".format(app_name,dict_key)
        returns = my_db.query(sql, state="one")
        return returns


    def updateResultByCaseId(self,response,is_pass,msg,case_id):
        """
        根据测试用例id，更新响应内容和测试内容
        """
        print("updateResultByCaseId")
        my_db = MysqlDb()
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        response = my_db.conn.escape_string(str(response))
        msg = my_db.conn.escape_string(msg)
        if is_pass:
            sql = "update `testcaseapp_case` set response='{0}', pass_or_not='{1}', msg='{2}', update_time='{3}' where id={4}".format("",is_pass,msg,current_time,case_id)
        else:
            sql = "update `testcaseapp_case` set response=\"{0}\", pass_or_not='{1}', msg='{2}', update_time='{3}' where id={4}".format(response,is_pass,msg,current_time,case_id)
        rows = my_db.execute(sql)
        return rows
    # def runAllCase(self,caseListId,api_host_obj="None",access_token ="None", last_response = ""):
    #     """
    #     执行全部用例的入口
    #     """
    #     print("runAllCase")
        
    #     #获取接口的域名 return{'id': 1, 'name': '云账本', 'dict_key': 'yzb_test_host', 'dict_value': 'https://tyqbapi.pmm2020.com'}
    #     # api_host_obj = self.loadConfigByAppAndKey(app_name,host_key)
    #     #获取全部用例
    #     # caseArr = self.loadAllClassByApp(app_name_id = api_host_obj["id"])
    #     caseArr = []
    #     for case_id in caseListId: #需要执行的所有用例id
    #         case = self.findCaseById(case_id)
    #         caseArr.append(case)
    #     # print(caseArr)
        
    #     #循环执行用例
    #     for case in caseArr:
    #         try:
    #             #执行用例
    #             response = self.runCase(case,api_host_obj,last_response,loginData)
                
    #             #断言判断
    #             assert_msg = self.assertResponse2(case, response)
    #             print("断言====",assert_msg)
    #             if assert_msg.get("is_pass") == True:
    #                 response.success()
    #                 self.last_response = response.text
    #                 print("响应成功===self.last_response=",self.last_response)
    #             else:
    #                 response.failure("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
    #                 print("url:{}--接口名称:{}--响应码:{}".format(case["url"], case["title"]+case["url"],response))
    #             #更新结果，储存数据库
    #             # rows = self.updateResultByCaseId(reponse, assert_msg["is_pass"], assert_msg["msg"], case["id"])
    #             # if rows:
    #             #     print("更新完成")
    #             # else:
    #             #     print("XXXXXX更新失败！XXXXXX")
    #         except Exception as e:
    #             print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

    #     #发送测试报告
    #     # self.sendTestReport(app_name = api_host_obj["name"])



    def runCase(self,case,headers,last_response,api_host_obj,loginData):
        """
        执行单个用例
        """
        
        
        request_data = json.loads(case.get("request_data"))
        method = case["method"]
        req_url = case["url"]
        #是否有前置条件
        if case.get("pre_case_id") > -1:
            print("需要前置用例返回值")
            json_data = {}
            if case.get("pre_case_id") == 5:
               json_data = loginData
            else:
                json_data = last_response.get("data")
            result = {}
            #根据前用例的断言方式确定返回值的格式
            if isinstance(json_data,list):
                result = random.choice(json_data)
            elif "list" in json_data:
                if len(json_data.get("list")) > 0:
                    arr_list = json_data.get("list")
                    result = random.choice(arr_list)
                elif len(json_data.get("list")) == 0:
                    return 0
                else:
                    print("见鬼了")
            elif "item" in json_data:
                if len(json_data.get("item")) > 0:
                    arr_item = json_data.get("item")
                    result = random.choice(arr_item)
                elif len(json_data.get("item")) == 0:
                    return 0
                else:
                    print("见鬼了")
            else:
                result = json_data
            pre_fields = json.loads(case.get("pre_fields"))
            for pre_field in pre_fields:
                if pre_field["scope"] == "header":
                    #遍历headers,替换对应的字段值，即寻找同名的字段
                    for header in headers:
                        field_names = pre_field["field"]
                        for key in field_names: #获取key
                            if header == key:
                                field_value = result[field_names[key]]
                                headers[key] = field_value
                elif pre_field["scope"] == "body":
                    #遍历headers,替换对应的字段值，即寻找同名的字段
                    for data in request_data:
                        field_names = pre_field["field"]
                        for key in field_names:
                            if data == key:
                                field_value = result[field_names[key]]
                                request_data[key] = str(field_value)
                elif pre_field["scope"] == "variable":
                    for data in request_data:
                        field_names = pre_field["field"]
                        for key in field_names:
                            if data == key:
                                field_value = result[field_names[key]]
                                passport = re.search("passport=(.*)", str(field_value)).group(1)
                                request_data[key] = passport
        if "access_token" in request_data:
            request_data['access_token'] = loginData["access_token"]
        if 'timestamp' in request_data:
            request_data['timestamp'] = str(int(time.time()))
        if isinstance(api_host_obj,str):
            api_host_obj = json.loads(api_host_obj)
        host_values = json.loads(api_host_obj["dict_value"])
        if case['domain_type'] == 0:
            header = json.loads(case.get("headers"))
            headers["Content-Type"] = header["Content-Type"]
            domain_host = host_values["native_host"]
            sign = GetDataSign().sign_body(req_url, request_data, api_host_obj["api_key"] ) 
            request_data["sign"] = sign
        elif case['domain_type'] == 1:
            domain_host = host_values["api_h5"]
            headers = json.loads(case.get("headers"))
        elif case['domain_type'] == 2:
            domain_host = host_values["quiz_h5"]
            headers = json.loads(case.get("headers"))
        elif case['domain_type'] == 3:
            domain_host = host_values["deputy_h5"]
            headers = json.loads(case.get("headers"))
        else:
            print("域名写错了吧")
        req_url = domain_host+case["url"]
        req_urlName = case["title"] + case["url"]
        content_type = headers.get("content-type")
        req = LocustRequestUtil(self)
        response_text = req.requestMethod(case, req_url, req_urlName, method,headers=headers,param=request_data, content_type=content_type)
        return response_text


    

    # def assertResponse(self,case,response):
    #     """
    #     断言响应内容，更新用例执行情况
    #     """
    #     print("assertResponse")
    #     is_pass = False
    #     if not response:
    #         assert_msg = {'is_pass':is_pass,'msg':response.text}
    #         return assert_msg
    #     if response == 0:
    #         is_pass = True
    #         assert_msg = {'is_pass':is_pass,'msg':"列表数据为空", "len":0}
    #         return assert_msg
    #     assert_type = case["assert_type"]
    #     expect_result = json.loads(case["expect_result"])
        
    #     json_response = json.loads(response.text)
    #     res_data = json_response.get("data")

    #     mark = False
    #     for code in expect_result: #判断业务状态码
    #         if code == json_response.get("status") or str(code) == json_response.get("status"):
    #             mark = True
    #             break
    #     if mark:
    #         if assert_type == "status":
    #             # if res_data.get("access_token"):
    #             #     self.access_token = res_data.get("access_token")
    #             is_pass = True
    #             print("测试用例通过")
    #         # 判断列表数组长度
    #         elif assert_type == "data_list":
    #             data_array = res_data.get("list")
    #             if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
    #                 is_pass = True
    #                 print("测试用例通过")
    #             else:
    #                 is_pass = False
    #                 print("测试用例不通过data-list")
    #         elif assert_type == "data_array":
    #             if res_data is not None and len(res_data) >= 0:
    #                 is_pass = True
    #                 print("测试用例通过")
    #             else:
    #                 is_pass = False
    #                 print("测试用例不通过data_array")
    #         elif assert_type == "data_json":
    #             data = json_response.get("data")
    #             if data is not None and isinstance(data, dict) and len(data) > int(expect_result):
    #                 is_pass = True
    #                 print("测试用例通过")
    #             else:
    #                 is_pass = False
    #                 print("测试用例不通过data_json")
    #         elif assert_type == "data_item":
    #             data_array = res_data.get("item")
    #             if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
    #                 is_pass = True
    #                 print("测试用例通过")
    #             else:
    #                 is_pass = False
    #                 print("测试用例不通过data-item")
    #         else:
    #             print("测试用例data类型错误")
    #             is_pass = False
    #     msg = '模块:{0}, 标题:{1}, 断言类型:{2}, 响应:{3}'.format(case.get("module"), case.get("title"), assert_type, response)
    #     #拼装信息
    #     assert_msg = {'is_pass':is_pass,'msg':msg}
    #     return assert_msg

        

    def sendTestReport(self,app_name):
        """
        邮件发送测试报告
        """
        print("sendTestReport")
        #加载全部测试用例
        results = self.loadAllClassByApp(app_name)
        title = "云账本接口自动化测试报告"
        content = """
        <html>
            <head>
                <title>接口自动化测试报告</title>
            </head
            <body>
                <h4>{}接口测试报告:</h4>
                <table border="1">
                    <tr>
                        <th>编号</th>
                        <th>模块</th>
                        <th>标题</th>
                        <th>是否通过</th>
                        <th>备注</th>
                        <th>响应</th>
                    </tr>
                    {}
                </table>

            </body>
        </html
        """
        template = ""
        for case in results:
            template += "<tr><td>{0}</td><td>{1}</td><td>{2}</td><td>{3}</td><td>{4}</td><td>{5}</td></tr>".format(
                case["id"], case["module"], case["title"], case["pass_or_not"], case["msg"], case["response"]
            )
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        content = content.format(current_time,template)
        mail_host = self.loadConfigByAppAndKey(app_name, 'mail_host')["dict_value"]
        mail_sender = self.loadConfigByAppAndKey(app_name, 'mail_sender')["dict_value"]
        mail_auth_code = self.loadConfigByAppAndKey(app_name, 'mail_auth_code')["dict_value"]
        mail_receivers = self.loadConfigByAppAndKey(app_name, 'mail_receivers')["dict_value"].split(",")
        mail = SendMail(mail_host)
        mail.send(title,content,mail_sender,mail_auth_code,mail_receivers)


    def login(self,case,headers,last_response,api_host_obj,loginData):
        print("进入登录")
        try:
            mobile = self.user.queueData.get()  #获取队列里的数据
        except queue.Empty:                     #队列取空后，直接退出
            print('no data exist')
            exit(0)
        request_data = json.loads(case.get("request_data"))
        request_data["password"] = "c80d171b81624145618791d99107554a"
        request_data["mobile"] = str(mobile)
        request_data["device_tokens"] = "AvmIKnZ8c_tSlnOiJWiGgn8X6u2vx5Z8"+str(int(time.time() * 1000))
        if isinstance(api_host_obj,str):
            print("判断str并转换成json")
            api_host_obj = json.loads(api_host_obj)
        header = json.loads(case.get("headers"))
        headers["Content-Type"] = header["Content-Type"]
        method = case["method"]
        req_url = case["url"]
        if 'timestamp' in request_data:
            request_data['timestamp'] = str(int(time.time()))
        
        
        #是否有前置条件
        if case.get("pre_case_id") > -1:
            print("需要前置用例返回值")
            json_data = last_response.get("data")
            result = {}
            #根据前用例的断言方式确定返回值的格式
            if isinstance(json_data,list):
                result = random.choice(json_data)
            elif json_data.get("list") and len(json_data.get("list")) > 0:
                arr_list = json_data.get("list")
                result = random.choice(arr_list)
            elif json_data.get("item") and len(json_data.get("item")) > 0:
                arr_item = json_data.get("item")
                result = random.choice(arr_item)
            else:
                result = json_data
            pre_fields = json.loads(case.get("pre_fields"))
            for pre_field in pre_fields:
                if pre_field["scope"] == "header":
                    #遍历headers,替换对应的字段值，即寻找同名的字段
                    for header in headers:
                        field_names = pre_field["field"]
                        for key in field_names: #获取key
                            if header == key:
                                field_value = result[field_names[key]]
                                headers[key] = field_value
                elif pre_field["scope"] == "body":
                    #遍历headers,替换对应的字段值，即寻找同名的字段
                    for data in request_data:
                        field_names = pre_field["field"]
                        for key in field_names:
                            if data == key:
                                field_value = result[field_names[key]]
                                request_data[key] = str(field_value)
                elif pre_field["scope"] == "variable":
                    for data in request_data:
                        field_names = pre_field["field"]
                        for key in field_names:
                            if data == key:
                                field_value = result[field_names[key]]
                                passport = re.search("passport=(.*)", str(field_value)).group(1)
                                request_data[key] = passport

        if "access_token" in request_data:
            print("loginData[access_token]===================================================",loginData["access_token"])
            request_data['access_token'] = loginData["access_token"]
        host_values = json.loads(api_host_obj["dict_value"])
        if case['domain_type'] == 0:
            domain_host = host_values["native_host"]
            sign = GetDataSign().sign_body(req_url, request_data, api_host_obj["api_key"] ) 
            request_data["sign"] = sign
        elif case['domain_type'] == 1:
            domain_host = host_values["api_h5"]
        elif case['domain_type'] == 2:
            domain_host = host_values["quiz_h5"]
        elif case['domain_type'] == 3:
            domain_host = host_values["deputy_h5"]
        else:
            print("域名写错了吧")
        req_url = domain_host+case["url"]
        req_urlName = case["title"] + case["url"]
        content_type = headers.get("content-type")
        req = LocustRequestUtil(self)
        # print("headers=====",headers)
        # print("req_url=====",req_url)
        # print("request_data=====",request_data)
        response_text = req.requestMethod(case, req_url, req_urlName, method,headers=headers,param=request_data, content_type=content_type)
        return response_text    
            

            





