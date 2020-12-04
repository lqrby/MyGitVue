import hashlib
import time
from urllib import parse
from urllib.parse import quote
from urllib.parse import quote_plus
"""
1. 参数加时间戳然后对参数以key字典排序
2. 对参数中的非空标量转换成get形式的字符串，其中字典中的vule进行url转码
3. 拼接key
4. 拼接route_url
5. 对以上字符串进行md5加密,
6. 在参数中带入sign

"""

class GetDataSign:


    def sign_body(self,url,zc_data, apikey):
        '''请求body sign签名'''
        # print("zc_data==={}".format(zc_data))
        dictList = {}
        # zc_data = ["".join(i) for i in zc_data.items() if i[1] and i[0] != "sign"]
        # 1. 先把参数编码
        for i in zc_data.items():
            if (isinstance(i[1],str)) and (isinstance(i[0],str)) and (i[1] and i[0] != "sign"): #去空参
                # print("=========={}===={}".format(i[1],i[0]))
                dictList[i[0]] = str.encode(i[1])#self.url_bm(i[1])

        #排序 
        Listarr = zip(dictList.keys(), dictList.values())
        px = sorted(Listarr,key=lambda x:x[0] )
        # pxhstr_data = "&".join("{}={}".format(k,v) for k, v in px) #去除空参数
        dictobj = dict(px)  #把元组转换成字典类型
        #把冒号转换成等于号
        pxh_data=parse.urlencode(dictobj) 
        # print("pxh_data==={}".format(pxh_data))  
        #拼接
        signed_string = pxh_data+"&key="+self.url_bm(apikey)+"&route_url="+self.url_bm(url)
        # print("加密前 ==== {}".format(signed_string))
        signed_string = self.jiamimd5(signed_string)
        # print("签名====={}".format(signed_string.upper()))
        return signed_string.upper()

    def url_bm(self,canshu):
        return parse.quote_plus(str(canshu))
        



        # MD5加密
    def jiamimd5(self,src):
        m = hashlib.md5()
        m.update(src.encode('UTF-8'))
        return m.hexdigest()
    

  

# if __name__ == '__main__':
#     apikey = "12345678"  # 验证密钥，由开发提供

#     zc_data={
#             "password":	"defe12aad396f90e6b179c239de260d4",
#             "sms_code":	"123456",
#             "mobile":18810798208,
#             "device_tokens":"AkWsVNSPMcwhC6nAXITHbPyrv0YgG5nt1T0B8n79-lrN",
#             "timestamp" : int(time.time()),
#             "sign":	""
#         }
#     url = "v2/login/signup"
#     apikey="djakdgkadgkafddadfjaddgbadsbfhbdashbgfadssfhbh"
#     GetDataSign().sign_body(zc_data, url, apikey)