# -*- coding: utf-8 -*-
# import sys
# import ast
class WriteAndReadTextFile():
    
    # 写入txt,(a追加写入,w覆盖写入)
    def test_write_txt(self,path_url,txt):
        f = open(path_url, 'w', encoding='utf-8')
        f.write(txt)
        f.close()

    # 逐行读取全部txt：
    def readAll_txt(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        return '\n'.join(lines)

    # 只读取第一行txt：
    def readOneLine_txt(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readline()
            # 判断是否读取到内容
            # if not text:
            #     break
    
        return lines



    # 读取第一行,并删除该行txt：
    def readAndRemoveOneLine(self,path):
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            lines_list = list(lines)
            if len(lines_list)>0:
                line = lines_list[0]
                lines_list.remove(lines[0])
                f.close()
                with open(path,"w",encoding="utf-8") as f_w:
                    s = "".join(lines_list)
                    f_w.write(s)
                    f.close()
                    return line
            else:
                line = None
                print("=======实名文件为空，没有数据=====")

        
