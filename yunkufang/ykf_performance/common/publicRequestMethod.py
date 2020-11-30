from locust import HttpUser,task,TaskSet,between,events
import sys,json,time,random
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_performance")
class PublicRequest(TaskSet):

    def requestMethod(self,url,data,header):
        with self.client.post(url,data=data,headers=header,verify=False,allow_redirects=False,catch_response=True) as response:
            return response


    

    def publicRequest(self,url,urlName,public_data,header):
        # public_data = json.dumps(public_data)
        with self.client.post(url,data = public_data,headers=header,name=urlName+url,verify=False,allow_redirects=False,catch_response=True) as response:
            print("响应结果======{}".format(response.text))
            if "[200]" in str(response):
                result = json.loads(response.text)
                if 'status' in result and result["status"] == 200 or 'status' in result and result["status"] == "200":
                    time.sleep(random.randint(1,3))
                    response.success()
                    return result
                else:
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response.text))

            else:
                print("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response))
                response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response))
    
                    


