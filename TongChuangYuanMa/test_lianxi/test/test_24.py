# strobj = "<Response [200]>"
# if "200" in str(strobj):
#     print("666")
# else:
#     print(7896)




# 读取第一行,并删除该行txt：
def readAndRemoveOneLine(path,path2):
    name = "赵六"
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for i,item in enumerate(lines):
            item = name+str(i+1)+" "+item
            # print(item)
            with open(path2,"a+",encoding="utf-8") as f_w:
                f_w.write(item)
            
                # arrlist.append(item)
    # print(arrlist)
    # with open(path,"w",encoding="utf-8") as f_w:    
    #     f_w.write(str(arrlist))
                
            
            # print(len(lines))
        # return lines


        # if len(lines)>0:
        #     with open(path,"w",encoding="utf-8") as f_w:    
        #         s = "".join(lines_list)
        #         f_w.write(s)
        #         f.close()
        #         return line
        # else:
        #     line = None
        #     print("=======实名文件为空，没有数据=====")
if __name__ == '__main__':
    filename = "F:/myTestFile/TestObject/TongChuangYuanMa/yunqianbao/static/shenfenzheng_1.txt"
    filename2 = "F:/myTestFile/TestObject/TongChuangYuanMa/yunqianbao/static/shenfenzheng.txt"
    readAndRemoveOneLine(filename,filename2)
    # print("666====",line)