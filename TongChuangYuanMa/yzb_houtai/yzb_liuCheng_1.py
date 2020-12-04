from locust import HttpUser,task,TaskSet,between,events
import time,json,random,sys,queue,ast
<<<<<<< HEAD
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
=======
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748

class CXSCLiuCheng(TaskSet):
    def on_start(self):
        self.header = {
            "Host":"tht.bankft.com",
            "Connection":"keep-alive",
            "Origin":"https://tht.bankft.com",
            "Content-Type":"application/x-www-form-urlencoded",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Referer":"https://tht.bankft.com/user/user-medal/create",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7",
            "Cookie":"_wodfoa-hsdf=f7a9b88ec5fd78cacdd1c5f397d1be22da9334a90189b82c806e16ea1a7287eaa%3A2%3A%7Bi%3A0%3Bs%3A12%3A%22_wodfoa-hsdf%22%3Bi%3A1%3Bs%3A32%3A%22CgaqMj4s0-VmAArvu08DnKE25MHST0bU%22%3B%7D; yqb-manage=dd98b05d3efab252cbcd65bfc6fa1a2f"
                    
        }

        


    @task
    def liuCheng(self):
        url = "/user/user-medal/create"
        urlName = "修改勋章级别"
        for i in range(40002965,40003500):
            up_data = {
                "_wodfoa-hsdf":"idpM9WL71iMj8-gY17uyb8eqGAOyxf4R-lG8nXXrKz3KvS2EL5HiUBPevnWW-sAZspogR9yOuyPPHPTOIdtJaA==",
                "UserMedal[uid]":str(i),
                "UserMedal[grade]":"1",
                "UserMedal[content]":"测试发红包"
            }
            with self.client.post(url,data = up_data,headers=self.header,name=urlName+url,verify=False,allow_redirects=False,catch_response=True) as response:
                print("修改勋章级别响应结果-----{}".format(response.text))
                # if "[200]" in str(response):
                #     result = json.loads(response.text)
                #     if 'status' in result and result["status"] == 200 or 'status' in result and result["status"] == "200":
                #         time.sleep(random.randint(1,3))
                #         response.success()
                #         return result
                #     else:
                #         response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response.text))

                # else:
                #     print("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response))
                #     response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(urlName,url,public_data,response))

            

                                

class WebsiteUser(HttpUser):
    tasks = [CXSCLiuCheng]
    wait_time = between(1, 3)
    host = "https://tht.bankft.com"
    