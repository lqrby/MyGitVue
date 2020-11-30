import csv


filename='F:/myTestFile/TestObject/YouTime/report/example_requests.csv'
with open(filename,'r')as f:
    read=csv.reader(f)
    for index,info in enumerate(read):
        if index!=0:   #这里加判断
            print(info)   
            if info[3:4] != ['0']:
                print("失败啦!!!")