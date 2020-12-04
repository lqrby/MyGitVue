from fontTools.ttLib import TTFont

class FontFaceDecode: 
    
    def __init__(self,filename_1,filename_2,newXmlPath):
        self.filename_1 = filename_1
        self.filename_2 = filename_2
        self.newXmlPath = newXmlPath
    
    def returnNewDict(self):
        # font=TTFont(self.filename_1)
        
        # font.saveXML("E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file4.xml")
        # filename = "E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file.woff" 
        # filename2 = "E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
        font1=TTFont(self.filename_1)    #打开本地字体文件01.ttf
        uniList1=font1.getGlyphOrder()[2:]    #获取所有编码，去除前2个
        # print(uniList1)
        # obj_list1=font1.getGlyphNames()[1:-1]   #获取所有字符的对象，去除第一个和最后一个
        font2=TTFont(self.filename_2)       #打开访问网页新获得的字体文件02.ttf
        print("self.newXmlPath====",self.newXmlPath)
        font2.saveXML(self.newXmlPath)
        uniList2=font2.getGlyphOrder()[2:]
        print("uniList1=====",uniList1)
        print("uniList2=====",uniList2)
        #手动确认编码和数字之间的对应关系，保存到字典中
        oldDictList={
            "uniE80C":"4",
            "uniE836":"7", 
            "uniE8E7":"6",
            "uniEEEC":"3", 
            "uniEF1B":"0", 
            "uniF104":"2", 
            "uniF424":"5", 
            "uniF487":"1", 
            "uniF4AE":"9", 
            "uniF534":"8"
        }
        num  = (0,0)
        bianma = ""
        mark = []
        newDictList = {}
        font1_dict = {}  
        for uni1 in uniList1:
            # print(uni1)
            obj1 = font1['glyf'][uni1]
            ptArr1 = obj1.coordinates
            for uni2 in uniList2:
                obj2 = font2['glyf'][uni2].coordinates[0]
                if abs(ptArr1[0][0] - num[0]) > abs(ptArr1[0][0] - obj2[0]):
                    num=obj2
                    bianma=uni2
            # print("-------",oldDictList[uni1])
                # print("555==",num,bianma)
            # print("666==",num,bianma)
            # print("bianma====",oldDictList[uni1])
            newDictList[bianma] = oldDictList[uni1]
            print("bianma===",bianma)
            print("newDictList==={}=={}".format(newDictList[bianma],oldDictList[uni1]))
        return newDictList

if __name__ == "__main__":
    filename_1 = r"E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
    filename_2 = r"E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file4.woff" 
    newXmlPath = r"E:/myTestFile/TestObject/TongChuangYuanMa/txt_file/maoyan4.xml" 
    # print(newXmlPath)
    dictList = FontFaceDecode(filename_1,filename_2,newXmlPath).returnNewDict()
    print("最终结果===",dictList)