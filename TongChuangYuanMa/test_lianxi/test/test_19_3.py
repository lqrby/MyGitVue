from fontTools.ttLib import TTFont

class FontFaceDecode: 

    def __init__(self,filename_1,filename_2):
        self.filename_1 = filename_1
        self.filename_2 = filename_2
    
    def returnNewDict(self):
        # filename = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file.woff" 
        # filename2 = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
        font1=TTFont(self.filename_1)    #打开本地字体文件01.ttf
        uniList1=font1.getGlyphOrder()[2:]    #获取所有编码，去除前2个
        # obj_list1=font1.getGlyphNames()[1:-1]   #获取所有字符的对象，去除第一个和最后一个
        font2=TTFont(self.filename_2)       #打开访问网页新获得的字体文件02.ttf
        uniList2=font2.getGlyphOrder()[2:]
        #手动确认编码和数字之间的对应关系，保存到字典中
        dictList={
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
        dictList2 = {}
        font1_dict = {}  
        for uni2 in uniList2:
            obj2 = font2['glyf'][uni2]
            ptArr2 = obj2.coordinates
            for uni1 in uniList1:
                obj1_0 = font1['glyf'][uni1].coordinates[0]
                if abs(ptArr2[0][0] - num[0]) > abs(ptArr2[0][0] - obj1_0[0]):
                    num=obj1_0
                    bianma=uni1
            dictList2[bianma] = dictList[uni2]
        # print(dictList2)
        return dictList2

if __name__ == "__main__":
    filename = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file.woff" 
    filename2 = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
    aa = FontFaceDecode(filename,filename2).returnNewDict()
    print(aa)