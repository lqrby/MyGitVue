from locust import TaskSet
import time,sys,json,random
from faker import Faker
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from test_script.publicscript.publicRequestMethod import PublicRequest
# 定义用户行为
class PublicFunction(TaskSet):
    '''
    # 点赞  
    loginUser:登录用户
    praisedUser:被赞人
    "uid" : 被赞人id
    "action": 0 点赞 1 取消点赞,
    "id": 用户id/动态id/价值id,
    "type": 0 动态 1价值 2用户 3评论,
    '''    
    # @task(1)
    def dianZan(self,header,praisedUser):
        # action = 0
        # if 'islike' in praisedUser and praisedUser['islike'] == 0:
        #     action = 0   #取消点赞
        # else:
        #     action = 1  #点赞
        dianzanData = {
            "uid": praisedUser['uid'],
            "cuid": 0,
            "ctype": 0,
            "resource": 0,
            "action": praisedUser["islike"],
            "id": str(praisedUser['id']),
            "type": praisedUser['type'],
            "assignmentId": 4,
            "cid": ""
        }
        dz_url = "/gateway/member/like"
        dz_urlName = "点赞/取消点赞"
        return PublicRequest(self).publicRequest(dz_url, dz_urlName, dianzanData, header)

    
    # @task(1)  
    def FocusOnly(self,header,userItem):
        '''
        # 只关注，不取消关注  
        '''
        if userItem["code"] == 200 and "data" in userItem and userItem["data"]["isatten"] == 0:
            action_num = 1
            self.followUser(header,userItem,action_num)
            # self.interrupt()
        else:
            action_num = 0

    
      
    def followUser(self,header,userItem,action_num):
        '''
        # 关注和取消关注用户  
        '''
        if userItem:
            gzData = {
                "uid": userItem["data"]["uid"],  #被关注的人id int 类型
                "resource": 0,
                "action": action_num,
                "type": 0
            }
            gz_url = "/gateway/member/followback"
            gz_urlName = "关注用户/取消关注"
            return PublicRequest(self).publicRequest(gz_url, gz_urlName, gzData, header)


    
    