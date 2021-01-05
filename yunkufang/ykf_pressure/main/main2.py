'''
version: V2.0
Author: 学海无涯任我游
Date: 2020-12-18 10:52:39
LastEditors: 学海无涯任我游
LastEditTime: 2020-12-23 17:25:32
'''
from locust import task,between,TaskSet,HttpUser
from locust.contrib.fasthttp import FastHttpUser
import time, random
from fake_useragent import UserAgent #未安装
ua = UserAgent()
class MyTaskSet(TaskSet):
    	
	def on_start(self):
		self.headers = {
			'User-Agent': ua.random
		}

	@task
	def index(self):
		time.sleep(random.randint(1,1))
		response = self.client.get("/",headers=self.headers)

class MyUser(FastHttpUser):
	#设置时间间隔在 1~5秒之间
	tasks = [MyTaskSet]
	wait_time = between(0.1, 0.5)
	host = "https://www.baidu.com"
	