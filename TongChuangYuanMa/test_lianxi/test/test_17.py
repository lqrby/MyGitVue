import pandas as pd
import numpy as np
from pandas import Series,DataFrame
import ast

def merge_dict(detail_list):
    # for item in detail_list.items():
    #     for i in range(len(item)):
    #     str1 = item[i]
    #     print(str1,end=' ')
    # with open(r'C:/Users/renbaoyu/Desktop/ludan.txt', 'a') as f:
    #     f.write(str(detail_list))
    #     print("成功啦")
        # f.write('\r\t')
    # with open(r'C:/Users/renbaoyu/Desktop/ludan.txt', "r") as f:  # 打开文件
    #     data = f.read()  # 读取文件
    #     dictData = ast.literal_eval(data)
    #     # print("3333333333333333",type(dictData),dictData[0],dictData)
    #     # dictData.remove(dictData[0])
    #     print("============================789456123============",dictData)
    # print("suo you shu ju ====",detail_list)
    # print("我要删除======",detail_list[0])
    a = detail_list[0].pop(1)
    detail_list[0].clear()
    detail_list[0].append(a)
    # print(a)
    
    
    print("最终数据=====",detail_list)


if __name__ == "__main__":
    
    detail_list=[
        [
            {'运单号':"JDVE01374455918",'收件人手机':18723480815,'订单数量':3},
            {'运单号':"JDVE01374493420",'收件人手机':18723480815,'订单数量':10},
            {'运单号':"JDVE01374493826",'收件人手机':18723480815,'订单数量':16}
        ],[
            {'运单号':"JDVE01374493427",'收件人手机':18723480811,'订单数量':5},
            {'运单号':"JDVE01374495289",'收件人手机':18723480811,'订单数量':20}
        ],[
            {'运单号':"JDVE01374138792",'收件人手机':18723480814,'订单数量':18}
        ]
    ]
    dict7 =  merge_dict(detail_list)
    # print(dict7)

