# import pdb

# s = '2'
# pdb.set_trace() # 运行到这里会自动暂停
# n = int(s)

# print(10 / n)

import os,sys

# print(os.path.abspath('.'))
# print(sys.argv[0])
# print(os.getcwd() )
allfilelist = os.listdir(os.path.abspath('.'))
print(allfilelist)
for f in allfilelist:
    filepath=os.path.join(os.path.abspath('.'),f)
    if os.path.isdir(filepath):