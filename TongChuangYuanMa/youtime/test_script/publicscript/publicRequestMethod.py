from locust import TaskSet
import sys,json,time,random,os
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from Performance_Core.performance_log import loadLogger




class PublicRequest(TaskSet):

    def requestMethod(self,url,urlName,data,header):
        data = json.dumps(data)
        with self.client.post(url,data = data, headers = header,name = urlName+url,verify = False,allow_redirects=False,catch_response=True) as response:
            return response

    def publicRequest(self,url,urlName,public_data,header):
        public_data = json.dumps(public_data)
        with self.client.post(url,data = public_data,headers = header,name = urlName+url,verify = False,allow_redirects=False,catch_response=True) as response:
            # print("响应结果======{}".format(response.text))
            if "200" in str(response):
                result = json.loads(response.text)
                # if "code" in result and result["code"] == 200 or result["code"] == "200": #response.status_code == 200
                time.sleep(random.randint(1,3))
                response.success()
                return result
                #推荐使用这种方式统计一个接口的响应时间，准确性更高
            else:
                print("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response.text))
                response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response.text))
    
    
    
    
