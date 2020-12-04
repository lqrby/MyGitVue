# def fact(n):
#     if n==1:
#         return 1
#     return n * fact(n - 1)

# L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]

# def by_score(t):
#     return -t[1]
# def by_name(t):
#     # print(t[0],t[1])
#     return(t[1])
# L2 = sorted(L, key=by_name,reverse=True)
# L = ['bob', 'about', 'Zoo', 'Credit']
# L1 = sorted(L,key=str.lower)

# def calc_sum(*args):
#     ax = 0
#     for n in args:
#         ax = ax + n
#     return ax

# s = 3 #设置全局变量
# def createCounter():   
#     def counter():
#         global s #引用全局变量
#         s = s+1
#         return s
#     return counter
# counterA = createCounter()
# def createCounter():
#     s = [0] 
#     def counter():
#         s[0] = s[0]+1
#         return s[0]
#     return counter
def createCounter():
    a = 0
    def counter():
        nonlocal a
        a = a+1
        return a
    return counter
counterA = createCounter()

if __name__ == '__main__':

    # print(fact(5))
    # s = lazy_sum(5,2,3)
    print(counterA(),counterA(),counterA(),counterA()) #每次调用子函数，都是会保留上次s的值进行计算的
    print(counterA())
    # print(s(),s(),s())