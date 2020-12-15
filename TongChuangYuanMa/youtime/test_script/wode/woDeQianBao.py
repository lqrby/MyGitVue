from locust import TaskSet
import time,json,random,sys
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from test_script.publicscript.publicRequestMethod import PublicRequest






# 我的钱包
class WoDeQianBao(TaskSet):
    '''
    # 去审核  （获取审核任务）
    '''        
    # @task(1)  
    def quShenHe(self,header):
        qsh_url = "/gateway/member/openReview"
        qsh_urlName = "获取审核任务"
        qsh_res = PublicRequest(self).requestMethod(qsh_url, qsh_urlName, {}, header)
        return json.loads(qsh_res.text)
        
    '''
    # 提交审核结果  
    '''                
    def shenHe(self,header,reviewId):
        time.sleep(random.uniform(10,20))
        num = random.choice(["111","111","111","000","111","111","111","001","111","111","011","111","111","111","100","111","111","111","111","101","111","111","111","010","111","111","111"])
        sh_data = {
            "reviewResult": num,
            "reviewId": reviewId
        }
        sh_url = "/gateway/member/reviewResult"
        sh_urlName = "提交审核结果"
        shenHe_res =  PublicRequest(self).publicRequest(sh_url, sh_urlName, sh_data, header)
        if shenHe_res:
            print("审核完毕，坐等奖励！！！")
            time.sleep(random.uniform(0.1,2)) 
        
        

    '''
    # 账单列表
    '''  
    # @task(1) 
    def zhangDan_list(self,header):
        #账单列表
        zdList_ata = {
            "page": 1,
            "type": 0,
            "limit": 20
        }
        zdList_url = "/gateway/member/bill"
        zdList_urlName = "账单列表"
        return PublicRequest(self).publicRequest(zdList_url, zdList_urlName, zdList_ata, header)


    '''
    # 兑换原始股
    '''  
    # @task(1) 
    def duiHuan(self,header):
        #账单列表
        dhysg_url = "/gateway/member/accountinfo"
        dhysg_urlName = "兑换原始股"
        PublicRequest(self).publicRequest(dhysg_url, dhysg_urlName, {}, header)
        
            