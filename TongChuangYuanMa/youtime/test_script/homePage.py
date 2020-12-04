from locust import TaskSet
import json,sys,time,random
import os
import oss2
from faker import Faker
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from test_script.publicscript.publicRequestMethod import PublicRequest
from common.pictures import SelectPictures

class HomePage(TaskSet):
    # @task(1)
    # @seq_task(1)
    # 上传图片
    def fuJinDeRen_list(self,header):
        '''
        # 附近的人列表  
        ''' 
        fuJin_data = {
            "maxage": 100,
            "conste": 0,
            "minage": 12,
            "location": {
                "address": u"北京市通州区",
                "lat": 39.83877589,
                "lon": 116.44186175
            },
            "sex": 3,
            "dist": 1000000.0,
            "page": 1,
            "limit": 20
        }
        fuJin_url = "/gateway/member/nearbylist"
        fuJin_urlName = "附近的人列表"
        return PublicRequest(self).publicRequest(fuJin_url, fuJin_urlName, fuJin_data, header)

    
    # @task(1)  
    def fuJinDeRen_Detail(self,header,uid):
        '''
        # 查看人员详情  
        '''
        fuJinDetailID = {
            "uid":uid
        }
        fuJinDetail_url = "/gateway/member/userinfo"
        fuJinDetail_urlName = "人员详情"
        return PublicRequest(self).publicRequest(fuJinDetail_url, fuJinDetail_urlName, fuJinDetailID, header)


    
    # @task(1)
    # @seq_task(1)
    def fuJinDongTai_list(self,header,loginUser):
        '''
        # 附近动态列表  
        '''    
        dt_data = {
            "qtime": int(round(time.time() * 1000)),
            "limit": 20,
            "location": loginUser["location"],
            "page": 1
        }
        dt_url = "/gateway/member/nearbydynamic"
        dt_urlName = "附近动态列表"
        return PublicRequest(self).publicRequest(dt_url, dt_urlName, dt_data, header)
        


    
    # @task(1)  
    def fuJinDongTai_Detail(self,header,praisedUser):
        '''
        # 查看动态详情  
        '''
        fjdtDetailID = {
            "location": {
                "address": praisedUser["location"],
                "lon": praisedUser["dlocation"]["lon"],
                "lat": praisedUser["dlocation"]["lat"]
            },
            "id": str(praisedUser["did"])
        }   
        fjdtDetail_url = "/gateway/member/dyInfo"
        fjdtDetail_urlName = "动态详情"
        return PublicRequest(self).publicRequest(fjdtDetail_url, fjdtDetail_urlName, fjdtDetailID, header)
        


    
    # @task(1)
    # @seq_task(1)
    def newDynamics(self,header):
        '''
        # 发布动态  
        dynamics
        '''    
        fake = Faker("zh_CN")
        # lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
        # lat = lonAndLat[0]
        # lon = lonAndLat[1]
        lat = round(random.uniform(37, 41), 14)#lonAndLat[0]
        lon = round(random.uniform(112, 119), 14)#lonAndLat[1]
        picArr = []
        power_data = self.getPicturePermission(header)
        power = power_data["data"]
        if 'status' in power and power["status"] == 0:
           picArr = SelectPictures(self).dongTaiPicture()
            # pictureArr,imgdir = self.get_picture()
            # picArr = random.sample(pictureArr,random.randint(1,10))
            # picArr2 = []
            # for pic in picArr:
            #     picstr = imgdir +"/"+ pic
            #     picArr2.append(picstr)
        newdtData = {
            "noticeusersid": 0,
            "seeby": 0,
            "location": {
                "address": fake.company(),
                "lon": float(lon),  #fake.longitude()
                "lat": float(lat) # fake.latitude()
            },
            "avatar": picArr,
            "contentType": 2,
            "content": self.Filter_sensitiveWords(fake.sentence(nb_words=6, variable_nb_words=True, ext_word_list=None))
        }
        newdt_url = "/gateway/member/pushdynamic"
        newdt_urlName = "发布动态"
        return PublicRequest(self).publicRequest(newdt_url, newdt_urlName, newdtData, header)

    
    def getPicturePermission(self,header):
        """
        获取发送动态图片的权限
        """
        getPower_url = "/gateway/member/aicidentify"
        getPower_urlName = "获取发送动态图片的权限"
        return PublicRequest(self).publicRequest(getPower_url, getPower_urlName, {}, header)


        
    # @task(1)
    # @seq_task(1)
    def fuJinJiaZhi_list(self,header,loginUser):
        '''
        # 附近价值列表  
        '''
        jz_data = {
            "assort": [],
            "qtime": int(round(time.time() * 1000)),
            "search": "",
            "limit": 20,
            "location": loginUser["location"],
            "page": 1,
            "type": 0
        }
        jz_url = "/gateway/member/nearbyvalue"
        jz_urlName = "价值列表"
        return PublicRequest(self).publicRequest(jz_url, jz_urlName, jz_data, header)
        


    
    # @task(1)  
    def fuJinJiaZhi_Detail(self,header,praisedUser):
        '''
        # 查看价值详情  
        '''
        jzDetail_data = {
            "location": praisedUser["wlLocationVo"],
            "id": str(praisedUser["wid"])
        }   
        jzDetail_url = "/gateway/member/goodsInfo"
        jzDetail_urlName = "价值详情"
        return PublicRequest(self).publicRequest(jzDetail_url, jzDetail_urlName, jzDetail_data, header)


      
    # @task(1)
    # @seq_task(1)
    def publishingValue(self,header,userId):
        '''
        # 发布价值  
        '''  
        fake = Faker("zh_CN")
        # lonAndLat = fake.local_latlng(country_code="CN", coords_only=False)
        lat = round(random.uniform(37, 41), 14)#lonAndLat[0]
        lon = round(random.uniform(112, 119), 14)#lonAndLat[1]
        #生成随机数，浮点类型
        tpyzm_res = self.coverCode(header)
        images,millis = self.uploadoss(self.generateSign(header),userId)
        kssj = time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
        print("起始时间:{}".format(kssj)) 
        title = self.Filter_sensitiveWords(fake.company_prefix()) #书籍名称
        demo = self.Filter_sensitiveWords(fake.text(max_nb_chars=200, ext_word_list=None)) #书籍简介
        jssj = time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
        print("结束时间:",jssj)
        # print("总共耗时:",jssj - kssj)
        fjz_data = {
            "images":images,
            "code": tpyzm_res["data"]["smsCode"],
            "wid": 0,
            "price": round(random.uniform(1, 200), 2),
            "ctime": millis,
            "location": {
                "address": fake.company(),
                "lon": float(lon),
                "lat": float(lat)
            },
            "exchangetype": 1,
            "title": title,
            "category": 5,
            "type": 0,
            "demo": demo
        }
        fjz_url = "/gateway/member/addgoods"
        fjz_urlName = "发布价值"
        time.sleep(random.randint(10,30))
        return PublicRequest(self).publicRequest(fjz_url, fjz_urlName, fjz_data, header)
        
    
    
    def coverCode(self,header):
        """
        获取封面验证码
        """
        hqyzm_url = "/gateway/member/getcode"
        hqyzm_urlName = "获取封面验证码"
        return PublicRequest(self).publicRequest(hqyzm_url, hqyzm_urlName, {}, header)

    def uploadoss(self,generateSign,userId):#localfile,remotePath,
        '''
        本地图片上传阿里云
        userId
        generateSign
        '''
        accessKeySecret = generateSign["data"]["accessKeySecret"]
        securityToken = generateSign["data"]["securityToken"]
        accesskeyId = generateSign["data"]["accessKeyId"]
        # millis = generateSign["data"]["expiration"]
        bucket_name = 'youtime-test'
        endpoint = 'oss-cn-beijing.aliyuncs.com'
        # 创建存储空间实例，所有文件相关的方法都需要通过存储空间实例来调用。
        # ossAuth = oss2.Auth(accesskeyId, accessKeySecret)
        ossAuth = oss2.StsAuth(accesskeyId, accessKeySecret,securityToken)
        bucket = oss2.Bucket(ossAuth, endpoint, bucket_name) #enable_crc=False
        # 上传图片
        pictures,imgdir = self.get_picture()
        imgArr = random.sample(pictures,3)
        print("imgArr===={}".format(imgArr))
        imgArr2 = []
        millis = int(round(time.time() * 1000))
        for i, img_path in enumerate(imgArr):
            key = "{}{}{}.png".format(str(millis),str(userId),str(i+1))
            bucket.put_object_from_file(key, imgdir+"/"+img_path)
            # print("result===={}==={}".format(key,result.status))
            # 生成带签名的URL，并指定过期时间为10分钟。过期时间单位是秒。
            style = 'image/resize,m_fixed,w_100,h_100/rotate,90'
            url = bucket.sign_url('GET', key, 10 * 60, params={'x-oss-process': style})
            # ret = bucket.sign_url('GET', key, 60*60*24)  # 返回值为链接，参数依次为，方法/oss上文件路径/过期时间(s)
            imgArr2.append(url.split("?")[0])
        print("价值图片===={}".format(imgArr2))
        return imgArr2,millis
    
    def get_picture(self):
        """
        获取图片文件夹中所有图片地址
        """
        imgdir = "F:/myTestFile/TestObject/YouTime/img/jiazhi"
        return os.listdir(imgdir),imgdir


    def Filter_sensitiveWords(self,text):
        """
        过滤敏感词
        """
        name_list = ["投资", "交易", "测试"]
        for name in name_list:
            if name in text:
                text = text.replace(name,"")
        return text

    
    def generateSign(self,header):
        '''
        "获取阿里云签名"
        '''
        hqaly_url = "/gateway/member/generateSign"
        hqaly_urlName = "获取阿里云签名"
        return PublicRequest(self).publicRequest(hqaly_url, hqaly_urlName, {}, header)




        
        
            

