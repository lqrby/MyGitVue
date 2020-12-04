from locust import TaskSet
import time,json,random,sys,queue
<<<<<<< HEAD
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
=======
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicRequestMethod import PublicRequest
from yunkufang.ykf_login import UserLogin


class YKFSouYe(TaskSet):

    def yrl_list(self,token,header):
        '''
        # 已认领商铺列表
        '''        
        list_url = "https://test-api.518aic.com/app/search/store"
        list_urlName = "已认领商铺列表"
        list_data = {
            "lng":"116.359658",
            "city":"北京市",
            "count":"15",
            "page":"1",
            "type":"1",
            "lat":"39.76106",
            "token":token
        }
        with self.client.post(list_url,data = list_data, headers = header,name = list_urlName+list_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                result = json.loads(response.text)
                if "status" in result and result["status"] == 200:
                    response.success()
                    return result
                else:
                    response.failure("报错url==={}-{} ，报错原因==={}{}".format(list_urlName,list_url,response,response.text))
            else:
                response.failure("服务器错误 ，请求url==={}-{},严重报错原因==={}===={}".format(list_urlName,list_url,response,response.text))   

