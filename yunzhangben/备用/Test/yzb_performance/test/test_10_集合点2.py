from locust import HttpUser,task,TaskSet,between,events
from gevent._semaphore import Semaphore
all_locusts_spawned = Semaphore() #计数器
all_locusts_spawned.acquire() #计数器为0时阻塞线程 每当调用acquire()时，内置计数器-1

def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() #内置计数器+1

events.hatch_complete += on_hatch_complete


class UserBehavior(TaskSet):
    @task(2)
    def index(self):
        print("0000000")
        self.client.get("/@12956929,4807514,13z")
        print("11111111")
        

    @task(1)
    def profile(self):
        print("开始集合--------------------")
        all_locusts_spawned.wait(timeout=60) #在此设置了集合点
        print("释放集合 200----------------")
        self.client.get("/")
        print("执行profile方法完毕")

    # def on_start(self):
    #     print("只执行一次")
    # #     print("开始")
    # #     all_locusts_spawned.wait() #在此设置了集合点
    # #     print("结束 200")
        

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)
    host = "https://www.baidu.com/"

if __name__ == '__main__':
    import os
    os.system("locust -f ./yunqianbao/test/test_10_集合点2.py")
