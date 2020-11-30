import random
from locust import HttpUser,TaskSet, task, between





class CXSCLiuCheng(TaskSet):
    @task
    def index_page(self):
        self.client.get("/")

    def on_start(self):
        print("66666")

class MyUser(HttpUser):
    tasks = [CXSCLiuCheng]
    wait_time = between(5,9)
    host = "https://www.baidu.com"