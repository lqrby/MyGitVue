
import requests
from requests_toolbelt import MultipartEncoder


class RequestUtil:

    def __init__(self):
        pass

    def customRequest(self, url, method, headers=None, param=None, content_type=None):
        """
        通用请求工具类
        """
        try:
            if method == "get":
                result = requests.get(url=url, params=param, headers=headers, verify= False)
                if "200" in str(result):
                    result.encoding = "utf-8"
                    return result.text
                else:
                    print("状态码错误：{}".format(result))

            elif method == "post":
                if content_type == "application/json":
                    result = requests.post(url=url, json=param, headers=headers, verify= False)
                    if "200" in str(result):
                        result.encoding = "utf-8"
                        return result.text
                    else:
                        print("状态码错误：{}".format(result))

                elif content_type == "multipart/form-data":
                    m = MultipartEncoder(param)
                    headers['Content-Type'] = m.content_type
                    result = requests.post(url=url, data=m, headers=headers, verify= False)
                    if "200" in str(result):
                        result.encoding = "utf-8"
                        return result.text
                    else:
                        print("状态码错误：{}".format(result))

                elif content_type == "text/xml":
                    result = requests.post(url=url, json=param, headers=headers, verify= False)
                    if "200" in str(result):
                        result.encoding = "utf-8"
                        return result.text
                    else:
                        print("状态码错误：{}".format(result))

                else:
                    # print("11144444444",url,param,headers) verify= False 关闭抓包代理
                    result = requests.post(url=url, data=param, headers=headers, verify=False)
                    if "200" in str(result):
                        result.encoding = "utf-8"
                        return result.text
                    else:
                        print("状态码错误：{}".format(result))
                        
            else:
                print("http method not allowed")

        except Exception as e:
            print("http请求报错:{0}".format(e))

if __name__ == "__main__":
    url = "https://xdclass.net/#/personalcenter"
    r = RequestUtil()
    header = {
        "Connection":"keep-alive",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    }
    results = r.customRequest(url,'get', headers=header)
    print(results)