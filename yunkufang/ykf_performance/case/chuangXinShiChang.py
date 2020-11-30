from locust import TaskSet
import time,json,random,sys
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunkufang/ykf_performance")
from common.QueryUsers import queryUsers
from common.publicRequestMethod import PublicRequest


class ChuangXinShiChang(TaskSet):

    # @task 
    def cxsc_list(self,token,header):
        '''
        # 创新市场列表
        '''        
        list_url = "https://test-innovate.518aic.com/shop/innovate-project/project-sale-list"
        list_urlName = "创新市场列表"
        list_data = {
            "count":20,
            "page":1,
            "type":0,
            "order_type":0,
            "token":token
        }
        with self.client.post(list_url,data = list_data, headers = header,name = list_urlName+list_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                if "status" in response.text:
                    result = json.loads(response.text)
                    if "status" in result and result["status"] == 200:
                        response.success()
                        return result
                    else:
                        response.failure("报错url==={}-{} ，报错原因==={}{}".format(list_urlName,list_url,response,response.text))
                else:
                    response.failure("严重报错url==={}-{},严重报错原因==={}===={}".format(list_urlName,list_url,response,response.text))   
            else:
                response.failure("服务器错误 ，请求url==={}-{},严重报错原因==={}===={}".format(list_urlName,list_url,response,response.text))   

    # @task 
    def cxsc_detail(self,project_id,token,header):
        '''
        # 创新市场详情
        '''    
        # detailObj = random.choice(cxsclist["data"]["list"])
        # print("xiangqing对象====",detailObj)
        detail_url = "https://test-innovate.518aic.com/shop/innovate-project/project-details"
        detail_urlName = "创新市场详情"
        detail_data = {
            "project_id":project_id,
            "token":token
        }
        with self.client.post(detail_url,data = detail_data, headers = header,name = detail_urlName+detail_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                detail = json.loads(response.text)
                if "status" in detail and detail["status"] == 200:
                    response.success()
                    return detail
                else:
                    response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(detail_urlName,detail_url,detail_data,detail))
            else:
                response.failure("服务器响应错误==={}=={}".format(response,response.text))

    # @task
    def quRenGou(self,detaill_obj,token,header):
        '''
        去认购
        '''
        # is_sold_out = detaill_obj["data"]["is_sold_out"]
        # if is_sold_out == 0:
        pay_status = detaill_obj["data"]["pay_status"]
        if pay_status == 0:
            qrg_url = "https://test-innovate.518aic.com/shop/innovate-payment/sale-info"
            qrg_urlName = "去认购"
            qrg_data = {
                "project_id":detaill_obj["data"]['id'],
                "token":token
            }
            with self.client.post(qrg_url,data = qrg_data, headers = header,name = qrg_urlName+qrg_url,verify = False,allow_redirects=False,catch_response=True) as response:
                    if "200" in str(response):
                        qrg = json.loads(response.text)
                        if "status" in qrg and qrg["status"] == 200:
                            response.success()
                            return qrg
                        else:
                            response.failure("报错url==={}-{} ，参数==={} ，报错原因==={}".format(qrg_urlName,qrg_url,qrg_data,qrg))
                    else:
                        response.failure("服务器响应错误==={}=={}".format(response,response.text))
        elif pay_status == 1:
            # response.success()
            print("已售罄")
        elif pay_status == 2:
            print("今日已售罄")
        elif pay_status == 3:
            print("已休市===",detaill_obj["data"]["message"])
        else:
            print("重点确认pay_status===================>>>",detaill_obj["data"]["pay_status"])
    
    



    # @task(1)
    def renGou(self,qurengou,detaill_obj_id,token,header):
        '''
        认购提交订单
        '''
        rg_url = "https://test-innovate.518aic.com/shop/innovate-payment/sale-order"
        rg_urlName = "认购提交订单"
        rg_data = {
            "project_id":detaill_obj_id,
            "num":random.randint(1,qurengou["data"]["goods"]["sale_num"]),
            "token":token
        }
        with self.client.post(rg_url,data = rg_data, headers = header,name = rg_urlName+rg_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "200" in str(response):
                rg = json.loads(response.text)
                if "status" in rg and rg["status"] == 200:
                    response.success()
                    return rg
                else:
                    response.failure("报错url==={}{}，报错原因==={}".format(rg_urlName,rg_url,rg))
            else:
                response.failure("服务器报错，响应码是==={}".format(response))


