



def merge_dict(x,y):
    for k,v in x.items():
        # print("x===",k)
        if k in y.keys():
            # print("y=====",k)
            # if v != y.values():
            #     print("y.values()====",y.values())
            y[k] += v
        else:
            print("y2=====",k)
            y[k] = v

    return y



if __name__ == "__main__":
    dict1={'运单号':"JDVE01374455918",'收件人手机':18723480815,'订单数量':3}
    dict2={'运单号':"JDVE01374493420",'收件人手机':18723480815,'订单数量':10}
    dict3={'运单号':"JDVE01374493826",'收件人手机':18723480815,'订单数量':16}
    dict4={'运单号':"JDVE01374493427",'收件人手机':18723480811,'订单数量':5}
    dict5={'运单号':"JDVE01374495289",'收件人手机':18723480811,'订单数量':20}
    dict6={'运单号':"JDVE01374138792",'收件人手机':18723480814,'订单数量':18}
    dict7 =  merge_dict(dict1,dict2)
    print(dict3)

# x = { 'apple': "1", 'banana': "2" }
# y = { 'banana': 10, 'pear': 11 }
# from collections import Counter
# X,Y = Counter(x), Counter(y)
# z = dict(X+Y)
# print(z)