from gevent._semaphore import Semaphore
from locust import TaskSet,HttpUser,events,task
# from lxml import etree

all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire()
def on_spawning_complete(**kwargs):
    return all_locusts_spawned.release() # 创建钩子方法
events.spawning_complete += on_spawning_complete # 挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        
        self.login()
        

    
    @task
    def login(self):
        all_locusts_spawned.wait() # 限制在所有用户准备完成前处于等待状态
        html = self.client.get('/').text
        print("cheng gong ==",html)

class WebsiteUser(HttpUser):
    host = 'https://www.baidu.com'
    tasks = [UserBehavior ]
    min_wait = 1000
    max_wait = 3000