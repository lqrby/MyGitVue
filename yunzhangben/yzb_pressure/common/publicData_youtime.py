# from locust import TaskSet
# import sys
# sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
# from common.pictures import SelectPictures
# from test_script.souye.fuJinJiaZhi import FuJinJiaZhi
# import time
# import random
# import json
# from faker import Faker


# class PublicData(TaskSet):
#     """
#         新增（发布）动态数据
#     """
#     def addDongTaiData(self,header):
#         fake = Faker("zh_CN")
#         lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
#         # print("*********{}".format(lonAndLat))    
#         lat = lonAndLat[0]
#         lon = lonAndLat[1]
#         picArr = []
#         power = self.getPicturePermission(header)
#         if 'status' in power and power["status"] == 0:
#             for i in range(random.randint(0,10)):
#                 picArr.append(fake.image_url())
#         newdtData = {
#             "noticeusersid": 0,
#             "seeby": 0,
#             "location": {
#                 "address": fake.company(),
#                 "lon": float(lon),  #fake.longitude()
#                 "lat": float(lat) # fake.latitude()
#             },
#             "avatar": picArr,
#             "contentType": 2,
#             "content": fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None)
#         }
#         return newdtData


#     """
#         新增（发布）价值数据
#     """
#     def addJiaZhiData(self,header):
#         fake = Faker("zh_CN")
#         lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
#         lat = lonAndLat[0]
#         lon = lonAndLat[1]
#         #生成随机数，浮点类型
#         fjztData = {
#             "images":SelectPictures(self).jiaZhiPicture(),
#             "code": self.coverCode(header),
#             "wid": 0,
#             "price": round(random.uniform(1, 200), 2),
#             "ctime": int(round(time.time() * 1000)),
#             "location": {
#                 "address": fake.company(),
#                 "lon": float(lon),
#                 "lat": float(lat)
#             },
#             "exchangetype": 1,
#             "title": fake.company_prefix(),
#             "category": 5,
#             "type": 0,
#             "demo": fake.text(max_nb_chars=200, ext_word_list=None)
#         }
#         return fjztData

#     """
#         获取发送动态图片权限
#     """
#     def getPicturePermission(self,header):
#         with self.client.post("/gateway/member/aicidentify", data = {}, headers = header, verify = False, allow_redirects=False,catch_response=True) as response:
#             # time.sleep(random.randint(1,5))
#             power_res = json.loads(response.text)
#             if 'code' in power_res and power_res["code"] == 200:
#                 response.success()
#                 return power_res["data"]
#             else:
#                 print("XXX获取图片权限失败XXX,{}".format(power_res))
#                 response.failure("XXX附获取图片权限失败XXX,{}".format(power_res))
#                 # self.interrupt()

#     """
#         获取封面验证码
#     """
#     def coverCode(self,header):
#         with self.client.post("/gateway/member/getcode",data = {},headers = header,verify = False,allow_redirects = False, catch_response = True) as response:
#             fmyzm_res = json.loads(response.text)
#             if "code" in fmyzm_res and fmyzm_res["code"] == 200:
#                 response.success()
#                 # print("9999999999{}".format(fmyzm_res["data"]["smsCode"]))
#                 return fmyzm_res["data"]["smsCode"]
#             else:
#                 response.failure("XXX{}发动态报错XXX===={}".format(header["token"],fmyzm_res))    