import sys, datetime, json, time, random, re
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
from utils.db_util import MysqlDb
from utils.locust_request_util import LocustRequestUtil
from utils.send_mail import SendMail
from case.qianMing import GetDataSign
from locust import HttpUser,task,TaskSet,between,events


class ClassTestCase(TaskSet):

    def __init__(self):
        self.access_token = ""
        self.obj = {}
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
    def runAllCase(self,app_name,case_id,host_key="None"):
        """
        执行全部用例的入口
        """
        print("runAllCase")
        #获取接口的域名 return{'id': 1, 'name': '云账本', 'dict_key': 'yzb_test_host', 'dict_value': 'https://tyqbapi.pmm2020.com'}

        #获取配置对象（地址、测试环境、apikey）
        api_host_obj = self.loadConfigByAppAndKey(app_name,host_key)
        #根据用例id获取用例对象
        case = self.findCaseById(case_id)
        # print("case==",type(case),case)
        try:
            #执行用例
            response = self.runCase(case,api_host_obj, last_result = self.obj)
            print("response===",response)
            #断言判断
            assert_msg = self.assertResponse(case, response)
            # response = assert_msg["response"]
            if not assert_msg.get("is_pass"):
                #前置条件不通过直接返回
                assert_msg["msg"] = "前置条件不通过直接返回"+assert_msg["msg"]
                response.failure("url:{}--接口名称:{}--报错信息:{}".format(case["url"],case["title"],response.text))
                print("url:{}--接口名称:{}--报错信息:{}".format(case["url"],case["title"],response.text))
            else:
                response.success()
                self.obj = json.loads(response.text)
                # print("666==",case["assert_type"])
                self.obj["assert_type"] = case["assert_type"]
        except Exception as e:
            print("用例id={0},模块:{1},标题:{2}，执行报错:{3}".format(case["id"],case["module"],case["title"],e))

    
        

        


    def runCase(self,case, api_host_obj, last_result):
        """
        执行单个用例
        """
        print("runCase")
        #获取用例中的headers
        headers = json.loads(case.get("headers")) 
        #获取用例中的参数
        request_data = json.loads(case.get("request_data"))
        #设置参数中timestamp的值
        if 'timestamp' in request_data:
            request_data['timestamp'] = str(int(time.time()))
        #获取用例的提交方法    
        method = case["method"]
        #获取用例的地址 
        req_url = case["url"]
        #获取用例的名称 
        urlName = case["title"]
        
        #判断是否需要上一个用例返回的参数值
        if case.get("pre_case_id") > -1 and case.get("pre_fields") != {}:
            print("需要前置条件的参数")
            # pre_case_id = case.get("pre_case_id")
            # pre_case = self.findCaseById(pre_case_id)
            # assert_type = pre_case["assert_type"]
            # #递归调用
            # pre_response = self.runCase(pre_case,self.api_host_obj)
            #断言
            # pre_assert_msg = self.assertResponse(pre_case,pre_response)
            # response = pre_assert_msg["response"]
            # if not pre_assert_msg.get("is_pass"):
            #     #前置条件不通过直接返回
            #     pre_assert_msg["msg"] = "前置条件不通过直接返回"+pre_assert_msg["msg"]
            #     response.failure("url:{}--接口名称:{}--报错信息:{}".format(req_url,urlName,response.text))
            #     print("url:{}--接口名称:{}--报错信息:{}".format(req_url,urlName,response.text))
            #     return pre_assert_msg
            # else:
            #     response.success()
            
            #判断需要case的前置条件是哪个字段
            if last_result:
                assert_type = last_result["assert_type"]
                # json_response = json.loads(pre_response)
                json_data = last_result.get("data")
                result = {}
                if assert_type == "status":
                    result = json_data  
                elif assert_type == "data_array" and len(json_data) > 0:   
                    result = random.choice(json_data)
                elif assert_type == "data_list" and len(json_data.get("list")) > 0:
                    arr_list = json_data.get("list")
                    result = random.choice(arr_list)
                elif assert_type == "data_item" and len(json_data.get("item")) > 0:
                    arr_item = json_data.get("item")
                    result = random.choice(arr_item)
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
        #若不需要前置用例参数值直接运行这一步
        if "access_token" in request_data and request_data.get("access_token") == "":
            request_data['access_token'] = self.access_token
        req = LocustRequestUtil(self)
        sign = GetDataSign().sign_body(req_url, request_data, api_host_obj["api_key"] ) 
        request_data["sign"] = sign
        print("url=====",req_url)
        req_url = case["url"]
        urlName = case["title"]+case["url"] #self.api_host_obj["dict_value"] + 
        content_type = headers["Content-Type"]
        print("2222222=====",type(request_data),request_data)
        request_data = json.dumps(request_data)
        response = req.requestMethod(req_url, urlName, method, param=request_data, headers=headers, content_type=content_type)
        return response


    def assertResponse(self,case,response):
        """
        断言响应内容，更新用例执行情况
        """
        print("assertResponse")
        if response:
            json_response = json.loads(response.text)
            res_data = json_response.get("data")
            assert_type = case["assert_type"]
            expect_result = json.loads(case["expect_result"])
            is_pass = False
            mark = False
            for code in expect_result: #判断业务状态码
                if code == json_response.get("status") or str(code) == json_response.get("status"):
                    mark = True
                    break
            if mark:
                if assert_type == "status":
                    if res_data.get("access_token"):
                        self.access_token = res_data.get("access_token")
                    is_pass = True
                    print("测试用例通过")
                # 判断列表数组长度
                elif assert_type == "data_list":
                    data_array = res_data.get("list")
                    if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
                        is_pass = True
                        print("测试用例通过")
                    else:
                        is_pass = False
                        print("测试用例不通过data-list")
                elif assert_type == "data_array":
                    if res_data is not None and len(res_data) >= 0:
                        is_pass = True
                        print("测试用例通过")
                    else:
                        is_pass = False
                        print("测试用例不通过data_array")
                elif assert_type == "data_json":
                    data = json_response.get("data")
                    if data is not None and isinstance(data, dict) and len(data) > int(expect_result):
                        is_pass = True
                        print("测试用例通过")
                    else:
                        is_pass = False
                        print("测试用例不通过data_json")
                elif assert_type == "data_item":
                    data_array = res_data.get("item")
                    if data_array is not None and isinstance(data_array,list) and len(data_array) >= 0:
                        is_pass = True
                        print("测试用例通过")
                    else:
                        is_pass = False
                        print("测试用例不通过data-item")
                else:
                    print("测试用例data类型错误")
                    is_pass = False
        msg = '模块:{0}, 标题:{1}, 断言类型:{2}, 响应:{3}'.format(case.get("module"), case.get("title"), assert_type, response.text)
        #拼装信息
        assert_msg = {'is_pass':is_pass,'msg':msg,"assert_type":assert_type}
        return assert_msg

        

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





