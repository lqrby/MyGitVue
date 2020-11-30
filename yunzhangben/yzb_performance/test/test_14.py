import requests,time,json
from locust import HttpUser,task,TaskSet,between,events

class CeShiObj(TaskSet):

    @task
    def mypublicRequest(self):
            header ={
                "Connection":"keep-alive",
                "app-type":"android", #android
                "mobile-unid":str(int(round(time.time() * 100000))),
                "app-version":"5.5.4.1",
                "mobile-type":"HUAWEIALP-TL00(8.0.0)",
                "mobile-system":"android8.0.0",
                "device-tokens": "AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",  #
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 8.0.0; ALP-TL00 Build/HUAWEIALP-TL00)",
                "Content-Type":	"application/x-www-form-urlencoded",
            }
            urlName = "zabbix"
            url = "/"
            with self.client.get(url,headers = header,name = urlName+url,verify = False,allow_redirects=False,catch_response=True) as response:
                # print("响应结果======{}".format(response.text))
                # result = json.loads(response.text)
                resStr = response.text
                # print(type(resStr))
                # print(type(resStr.encode('utf-8')))
                print(resStr.encode('utf-8'))
                # print(resStr.decode('utf-8'))
                # if "code" in result and result["code"] == 200 or result["code"] == "200": #response.status_code == 200
                #     time.sleep(random.randint(1,3))
                #     response.success()
                #     return result
                #     #推荐使用这种方式统计一个接口的响应时间，准确性更高
                # else:
                #     print("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,result))
                #     response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,result))
                
class WebsiteUser(HttpUser):
    tasks = [CeShiObj]
    wait_time = between(1, 3)
    host = "http://192.168.200.155/"
    

