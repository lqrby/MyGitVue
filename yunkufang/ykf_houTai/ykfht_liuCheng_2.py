from locust import HttpUser,task,TaskSet,between,events
import time,json,random,sys,queue,ast
from bs4 import BeautifulSoup
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
# from Interface.QueryUsers import queryUsers
# from test_script.publicscript.publicRequestMethod import PublicRequest
from excel_group import ExcelGroup
from objecte import TiHuoJiLU


class CXSCLiuCheng(TaskSet):
    def on_start(self):
        self.header = {
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cookie":"_identity-backend=575bc09406a4575c26bcaaec869f6ff17312c529c77bed2519f1a756e6179343a%3A2%3A%7Bi%3A0%3Bs%3A17%3A%22_identity-backend%22%3Bi%3A1%3Bs%3A47%3A%22%5B34%2C%220m_rHWJKJ57X6kvyZQSY2GHbyYEP90e3%22%2C2592000%5D%22%3B%7D; advanced-backend=l0augj6it5d720grtu66vh1vm9; _csrf-backend=a746c6fabb87f0a5355498e0a878cacea7babda2230be6d76549d3388530c591a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf-backend%22%3Bi%3A1%3Bs%3A32%3A%22M6ThOt3XN42KkvCgyWLrf03LzozR1NNt%22%3B%7D"
        }
        self.excelFilePath = "C:/Users/renbaoyu/Desktop/8.21录单.xlsx"
        self.textFilePath = "C:/Users/renbaoyu/Desktop/ludan.txt"


    @task
    def liuCheng(self):
        mark = 0
        dictData = ExcelGroup.readText(self.textFilePath)
        arrobject = []
        if len(dictData)>0:
            oder = dictData[0]
            print("oder====",oder)
            mobile = oder[0]["收件人手机"]
            if "花生油" in oder[0]["物品名"]:
                arrobject = [34,35,42]
            elif "提灰枣" in oder[0]["物品名"]:
                arrobject = [20,2]
            else:
                arrobject = [34,35,42,20,2]
            for j in arrobject:
                print("项目id是====",j)
                tr = TiHuoJiLU(self).queryOderAndLuRu(int(mobile),j,self.header) #查询订单
                if tr:  #有待发货的订单
                    qfhobj = TiHuoJiLU(self).quFaHuo(tr,self.header) #去发货,
                    if qfhobj:
                        jg_num = TiHuoJiLU(self).faHuo(qfhobj,self.header,oder) #发货。携带oder对象是为了获取订单号总数
                        print("返回的发货数量是====",type(jg_num),jg_num)
                        if jg_num:
                            mark = 1
                            # 删除已发货的订单
                            print("发货成功！！！")
                            if len(oder) == jg_num:
                                del dictData[0]
                            else:
                                print("进入了这里了------------------重点关注")
                                o_arr2 = oder[:]
                                for ii,obj in enumerate(o_arr2):
                                    if ii < jg_num:
                                        sysl = oder.pop(jg_num-1)
                                        dictData[0].clear()
                                        dictData[0].append(sysl)
                    break   #返回值为假直接跳出循环，为真则继续往下执行代码，直到结束跳出循环
            if mark == 0:
                del dictData[0]
            ExcelGroup.writeText(self.textFilePath,dictData)
            print("重新把数据写入txt文件成功")
        else:
            print("**********************txt文件无数据******************")

            

                                

class WebsiteUser(HttpUser):
    tasks = [CXSCLiuCheng]
    wait_time = between(1, 3)
    host = "https://admin.518.518aic.com"
    