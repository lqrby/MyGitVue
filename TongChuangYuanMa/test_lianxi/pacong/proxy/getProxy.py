import requests,json, os
from bs4 import BeautifulSoup

class Proxy:

    def pingProxy(self,ip):
        """
        判断是否能ping通
        """
        print("ip====",ip)
        p=os.popen("ping {}".format(ip))
        x=p.read()
        p.close()
        if x.count('TTL'):
            return True
            # print("ping通了")
        else:
            # print("ping不通")
            return False

    def get_proxy(self,header,proxyurl,filePath):
        response = requests.get(proxyurl,headers = header)
        response.encoding = 'utf-8'
        result = response.text
        print(result)
        if "免费代理" in result:
            soup = BeautifulSoup(result, 'html.parser')
            tbody = soup.find('tbody')
            trArr = tbody.find_all("tr")
            proxyArr = []
            for tr in trArr:
                tdArr = []
                for td in tr.find_all("td"):
                    tdArr.append(td.string.strip())
                proxyArr.append(tdArr)
            goodIpArr = []
            for data in proxyArr:
                if self.pingProxy(data[0]):
                    goodIpArr.append(data)

            """
            把数据写入txt文件
            """
            with open(filePath, 'w') as f:
                f.write(str(goodIpArr))
                print("数据写入成功啦")
        else:
            print("XXXXXX获取代理ip失败XXXXXX{}".format(response))




    



if __name__ == '__main__':
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
    }
    proxyurl = "http://www.dailiip.cc/freedailiip/2020/0611/647.html"
    filePath = "F:/proxyList.txt"

    Proxy().get_proxy(header,proxyurl,filePath)
    