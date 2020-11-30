



def merge_dict(allOders):
    for 
    for k,v in x.items():
        if k in y.keys():
            y[k] += v
        else:
            y[k] = v

    return y



if __name__ == "__main__":
    dict1=[
        {'运单号':"JDVE01374455918",'收件人手机':18723480815,'订单数量':3},
        {'运单号':"JDVE01374493420",'收件人手机':18723480815,'订单数量':10},
        {'运单号':"JDVE01374493826",'收件人手机':18723480815,'订单数量':16},
        {'运单号':"JDVE01374493427",'收件人手机':18723480811,'订单数量':5},
        {'运单号':"JDVE01374495289",'收件人手机':18723480811,'订单数量':20},
        {'运单号':"JDVE01374138792",'收件人手机':18723480814,'订单数量':18}
    ]
    dict7 =  merge_dict(dict1)
    print(dict7)

# x = { 'apple': "1", 'banana': "2" }
# y = { 'banana': 10, 'pear': 11 }
# from collections import Counter
# X,Y = Counter(x), Counter(y)
# z = dict(X+Y)
# print(z)