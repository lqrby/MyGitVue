#-*- coding : utf-8 -*-
# coding: utf-8

from locust import TaskSet
import time
import random,unittest,logging
import queue
import json,sys,xlrd,openpyxl,csv
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
from Interface.QueryUsers import queryUsers
from test_script.publicscript.publicFunction import PublicFunction
from test_script.wode.woDeQianBao import WoDeQianBao
from Performance_Core.performance_log import loadLogger
import decimal
from faker import Faker
from common.pictures import SelectPictures
# from common.publicData import PublicData
from test_script.loginandregister.loginAndzhuCe import LoginAndZhuCe
from test_script.publicscript.publicFunction import PublicFunction
from test_script.homePage import HomePage
# from report.HTMLTestRunner import HTMLTestRunner
from report.HTMLTestRunner3 import data_analyse
from locust import events
from bs4 import BeautifulSoup
# 定义用户行为
class XunBaoShouYe(TaskSet):

    def xunBao_index(self,header,proxies):
        '''
        # 寻宝网首页 
        '''  
        xbsy_url = "/"
        xbsy_urlName = "寻宝网首页"
        # print("代理ip是===={}".format(proxies))
        with self.client.get(xbsy_url, headers = header,proxies = proxies, name = xbsy_urlName+xbsy_url,verify = False,allow_redirects=False,catch_response=True) as response:
            if "navigation" in response.text:
                soup = BeautifulSoup(response.text, 'html.parser')
                sy = soup.find('nav', attrs={'id': 'navigation'})
                response.success()
                return sy
            else:
                response.failure("报错url==={}{} ，报错原因==={}{}".format(xbsy_urlName,xbsy_url,response,response.text))
   
    # @task
    def xunBaoIndex_list(self,header,proxies):
        '''
        # 寻宝网首页list 
        ''' 
        # print("代理ip是2===={}".format(proxies)) 
        rg_url = "/hot_recommend.htm?key=ajax"
        rg_urlName = "寻宝网首页列表"
        with self.client.get(rg_url, headers = header, proxies = proxies, name = rg_urlName+rg_url,verify = False,allow_redirects=False,catch_response=True) as response:
                if "key_items" in response.text:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    pplist = soup.find_all('div', attrs={'class': 'lotitem-picture'})
                    response.success()
                    return pplist
                else:
                    response.failure("报错url==={}-{},报错原因==={}".format(rg_urlName,rg_url,response,response.text))


    def xunBaoIndex_detail(self,header,proxies,detail):
        '''
        # 详情
        '''  
        # print("代理ip是3===={}".format(proxies))
        if detail:
            a = detail.find('a')
            # print("a标签的href值是=====",a["href"])
        xb_url = a["href"]
        xb_urlName = "寻宝详情"
        with self.client.get(xb_url, headers = header, proxies = proxies, name = xb_urlName+xb_url,verify = False,allow_redirects=False,catch_response=True) as response:
                print(type(response.text))
                if "免责声明" in response.text:
                    print("请求详情成功")
                    # soup = BeautifulSoup(response.text, 'html.parser')
                    # pplist = soup.find('section', attrs={'class': 'key_items'})
                #     response.success()
                #     return pplist
                # else:
                #     response.failure("报错url==={}-{} ，报错原因==={}".format(rg_urlName,rg_url,pplist))
                

    
    
    
