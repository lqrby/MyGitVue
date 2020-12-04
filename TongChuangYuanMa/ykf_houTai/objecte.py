from locust import TaskSet
import time,json,random,sys,queue,re
import openpyxl,xlrd
from bs4 import BeautifulSoup
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
# from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicRequestMethod import PublicRequest
# from yunkufang.ykf_login import UserLogin
import pandas as pd
import numpy as np
from pandas import Series,DataFrame
from requests_toolbelt.multipart.encoder import MultipartEncoder



class TiHuoJiLU(TaskSet):

    def readExcel(self,filepath):
        #打开excel表，读取数据并转换成数组对象
        book = xlrd.open_workbook(filepath)
        #找到sheet页
        table = book.sheet_by_name("任保玉")
        #获取总行数总列数
        row_Num = table.nrows
        col_Num = table.ncols
        s =[]
        key =table.row_values(0)# 这是第一行数据，作为字典的key值
        if row_Num <= 1:
            print("没数据")
        else:
            j = 1
            for i in range(row_Num-1):
                d ={}
                values = table.row_values(j)
                for x in range(col_Num):
                    # 把key值对应的value赋值给key，每行循环
                    d[key[x]]=values[x]
                j+=1
                # 把字典加到列表中
                s.append(d)
            return s




    def merge_dict(self,detail_list):
        '''
        根据手机号分组数据
        '''
        goods_ids = set([i.get('收件人手机') for i in detail_list])
        # print(goods_ids)
        detail_list_group = []
        for x in goods_ids:
            temp = []
            for y in detail_list:
                if y.get('收件人手机') == x:
                    temp.append(y)
            if temp:
                detail_list_group.append(temp)
        # print(detail_list_group)
        return detail_list_group


    def queryOderAndLuRu(self,mobile,number,header):
        '''
        根据手机号查询订单
        '''
        query_url = "/innovate/project/voucher-list?id={}&Project%5Bmobile%5D=&Project%5Btel%5D={}".format(number,mobile)
        query_name = "根据手机号查询订单"
        with self.client.get(query_url,headers = header,name = query_name+query_url,verify = False,allow_redirects=False,catch_response=True) as response:
            result = response.text
            if "待发货" in result:
                soup = BeautifulSoup(result, 'html.parser')
                tbody = soup.find('tbody')
                all_tr = tbody.find_all('tr')
                for tr in all_tr:
                    if "待发货" in str(tr):
                        break
                response.success()
                return tr
            else:
                print("暂时无待发货的订单")


    def quFaHuo(self,tr_oder,header):
        """
        去发货
        """
        o_id = tr_oder.find("td").text   #订单id
        qfh_url = "/innovate/project/send-voucher?op_id={}".format(o_id)
        qfh_urlName = "去发货"
        with self.client.get(qfh_url, headers = header,name = qfh_urlName+qfh_url,verify = False,allow_redirects=False,catch_response=True) as response:
            result = response.text
            if "保存" in result:
                # print("========",result)
                response.success()
                return result
            else:
                response.failure("报错url==={}-{} ，报错原因==={}".format(qfh_urlName,qfh_url,result))   




    def faHuo(self,qfh_result,header,oder):
        """
        发货
        """
        print("进入了 发货 函数")
        csrf = re.compile(r'<meta name="csrf-token" content="(.*?)">').search(str(qfh_result)).group(1)
        print("csrf=====",csrf)
        soup = BeautifulSoup(qfh_result, 'html.parser')
        form = soup.find('form', attrs={'id':'w0'})
        div1 = form.find("div")
        oderId = div1.find(id = "store-id")["value"] #订单id
        objectId = div1.find(id = "store-project_id")["value"] #项目id
        userId = div1.find(id = "store-user_id")["value"] #用户id
        kuaiDi = oser[0]["快递名称"]
        print("快递名称========",kuaiDi)
        div3 = form.find_all("div")[4]
        labelNumber = div3.find_all("label")[1]
        label_number = int(labelNumber.text)
        beizhu = ""
        if label_number > 1:
            print("有备注")
            beizhu = "由于订单号太多录不下，5天内会陆陆续续到货，超过10天未到齐请及时与客服联系。"
        if len(oder) >= label_number:
            fh_url = "/innovate/project/save-voucher"
            fh_urlName = "发货"
            m = MultipartEncoder(
                fields = {
                    "Project[operate_id]" : str(oderId),
                    "Project[project_id]" : str(objectId),
                    "Project[user_id]" : str(userId),
                    "Project[shipping_type]" : str(label_number),
                    "Project[shipping_name]" : kuaiDi,
                    "Project[shipping_sn]" : oder[0]["运单号"],
                    "Project[shipping_desc]" : beizhu,
                    "_csrf-backend" : csrf,
                    "Project[shipping_status]" : "0"
                }
            )
            header["Content-Type"] = m.content_type
            with self.client.post(fh_url,data=m, headers = header,name = fh_urlName+fh_url,verify = False,allow_redirects=False,catch_response=True) as response:
                header["Content-Type"] = "text/html; charset=UTF-8"
                print("发货成功码是多少=====",response)
                if "302" in response:
                    response.success()
                    print("发货数量是=====",label_number)
                    return label_number
                else:
                    response.failure("报错url==={}-{} ，报错原因==={}".format(fh_urlName,fh_url,response.text))   
        else:
            print("*********系统发货数量大于excel总数量********{}".format(oder[0]["收件人手机"]))

    # @task 
    def thlb_list(self,header,number):
        '''
        # 提货列表
        '''        
        list_url = "/innovate/project/voucher-list?id=42".format(number)
        list_urlName = "提货列表"
        
        with self.client.get(list_url, headers = header,name = list_urlName+list_url,verify = False,allow_redirects=False,catch_response=True) as response:
            result = response.text
            if "grid-view" in result:
                # print("========",result)
                response.success()
                return result
            else:
                response.failure("报错url==={}-{} ，报错原因==={}".format(list_urlName,list_url,result))
            


  

    

