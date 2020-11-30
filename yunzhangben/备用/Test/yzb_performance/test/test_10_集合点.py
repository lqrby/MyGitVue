from locust import events
from gevent._semaphore import Semaphore  
all_locusts_spawned = Semaphore()
all_locusts_spawned.acquire() 

def on_hatch_complete(**kwargs):
    all_locusts_spawned.release() 

events.hatch_complete += on_hatch_complete  #挂载到locust钩子函数（所有的Locust实例产生完成时触发）

class TestTask(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()
        all_locusts_spawned.wait()