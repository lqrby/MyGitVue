from locust import HttpUser,task,TaskSet,between,events
import time,json,random,sys,queue
from bs4 import BeautifulSoup
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
# from Interface.QueryUsers import queryUsers
# from test_script.publicscript.publicRequestMethod import PublicRequest
from objecte import TiHuoJiLU



class CXSCLiuCheng(TaskSet):

   
    def on_start(self):
        self.header = {
            "Connection":"keep-alive",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Cookie":"_identity-backend=575bc09406a4575c26bcaaec869f6ff17312c529c77bed2519f1a756e6179343a%3A2%3A%7Bi%3A0%3Bs%3A17%3A%22_identity-backend%22%3Bi%3A1%3Bs%3A47%3A%22%5B34%2C%220m_rHWJKJ57X6kvyZQSY2GHbyYEP90e3%22%2C2592000%5D%22%3B%7D; advanced-backend=l0augj6it5d720grtu66vh1vm9; _csrf-backend=a746c6fabb87f0a5355498e0a878cacea7babda2230be6d76549d3388530c591a%3A2%3A%7Bi%3A0%3Bs%3A13%3A%22_csrf-backend%22%3Bi%3A1%3Bs%3A32%3A%22M6ThOt3XN42KkvCgyWLrf03LzozR1NNt%22%3B%7D"
        }
        


    @task
    def liuCheng(self):
        # cxsc_list = TiHuoJiLU(self).thlb_list(self.header,42)  #订单列表
        # arrobject = [42,34,35]
        arrobject = [2,20]
        filepath = "C:/Users/renbaoyu/Desktop/8.21录单.xlsx"
        excelList = TiHuoJiLU(self).readExcel(filepath) #获取excel
        odergroup = TiHuoJiLU(self).merge_dict(excelList)  #对表格数据分组
        odergroup2 = odergroup[:]
        for i,oder in enumerate(odergroup2): #遍历分组后的订单列表
            mobile = oder[0]["收件人手机"]
            for j in arrobject:
                queryoder = TiHuoJiLU(self).queryOderAndLuRu(int(mobile),j,self.header) #查询订单
                if queryoder:  #有待发货的订单
                    soup = BeautifulSoup(queryoder, 'html.parser')
                    tbody = soup.find('tbody')
                    all_tr = tbody.find_all('tr')
                    for tr in all_tr:
                        if "待发货" in str(tr):
                            qfhobj = TiHuoJiLU(self).quFaHuo(tr,self.header) #去发货,
                            if qfhobj:
                                try:
                                    jg = TiHuoJiLU(self).faHuo(qfhobj,self.header,oder) #携带oder对象是为了获取订单号总数
                                    if jg:
                                        # 删除已发货的订单
                                    if len(oder) == jg:
                                        odergroup.remove(oder)
                                    else:
                                        o_arr2 = oder[:]
                                        for ii,obj in enumerate(o_arr2):
                                            if ii < jg:
                                                oder.remove(obj)
                                                print("***************************",odergroup)
                                except Exception as e:
                                    print("异常信息:{}".format(e))
                                finally:
                                    pass
                                
                                


         
        


class WebsiteUser(HttpUser):
    tasks = [CXSCLiuCheng]
    wait_time = between(1, 3)
    host = "https://admin.518.518aic.com"
    # users = queryUsers(35,100) #多个用户
    # print(users)
    # users = [
    #     {'password': 'ren123456', 'mobile': '15001200238'},
    #     {'password': 'ren123456', 'mobile': '18810798467'},
    #     {'password': 'ren123456', 'mobile': '15000000545'},
    #     {'password': 'ren123456', 'mobile': '15000000546'},
    #     {'password': 'ren123456', 'mobile': '15000000547'},
    #     {'password': 'ren123456', 'mobile': '15000000548'},
    #     {'password': 'ren123456', 'mobile': '15000000551'},
    #     {'password': 'ren123456', 'mobile': '15000000550'},
    #     {'password': 'a123456789', 'mobile': '18246463219'},
    #     {'password': 'a123456789', 'mobile': '13314627183'},
    #     {'password': 'a123456789', 'mobile': '18704651002'},
    #     {'password': 'a123456789', 'mobile': '17600920288'},
    #     {'password': 'a123456789', 'mobile': '18410301111'},
    #     {'password': 'a123456789', 'mobile': '18410301112'},
    #     {'password': 'a123456789', 'mobile': '18410301113'},

    #     ] #单个用户
    # queueData = queue.Queue()
    # for user in users:
    #     queueData.put_nowait(user)   

    # def setup(self):
    #     print('locust setup')
 
    