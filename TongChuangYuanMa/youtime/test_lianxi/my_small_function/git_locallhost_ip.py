import socket

def get_host_ip():
    '''
    查询本机ip地址
    :return: ip
    '''
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        print(ip)
    finally:
        s.close()

get_host_ip()




"""
    获取本机公网ip地址
"""
import requests
import re

req=requests.get("http://txt.go.sohu.com/ip/soip")
ip=re.findall(r'\d+.\d+.\d+.\d+',req.text)
print(ip[0])
