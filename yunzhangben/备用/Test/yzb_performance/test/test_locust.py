# -*- coding: utf-8 -*-
import time
from locust import User, HttpUser, task, between,events

# class QuickstartUser(User):
#     wait_time = between(1, 2)

#     @task
#     def index_page(self):
#         self.client.get("/hello")
#         self.client.get("/world")

#     @task(3)
#     def view_item(self):
#         for item_id in range(10):
#             self.client.get(f"/item?id={item_id}", name="/item")
#             time.sleep(1)

#     def on_start(self):
#         print("executing my_task")

# if __name__ == "__main__":
#     QuickstartUser
print(events.spawning_complete)
