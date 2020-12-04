# -*- coding: utf-8 -*-

def person(name, age, *args, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
    print(args)

    

if __name__ == "__main__":
    name = '张三'
    age = 18
    gender = '男'
    address = '北京市朝阳区'
    a = "123"
    b = '456'
    person(name, age, gender,address,b = a,a=b)
