from fontTools.ttLib import TTFont

class FontFaceDecode: 
    
    def __init__(self,filename_1,filename_2,newXmlPath):
        self.filename_1 = filename_1
        self.filename_2 = filename_2
        self.newXmlPath = newXmlPath
    
    def returnNewDict(self):
        font1=TTFont(self.filename_1)    #打开本地字体文件01.ttf
        uniList1=font1.getGlyphOrder()[2:]    #获取所有编码，去除前2个
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
            obj1 = font1['glyf'][uni1].coordinates[0]
            for uni2 in uniList2:
                obj2 = font2['glyf'][uni2].coordinates[0]
                if abs(obj1[0] - num[0]) > abs(obj1[0] - obj2[0]):
                    num=obj2
                    bianma=uni2
                print("aa = {},bb ==== {},cc ===={}, dd ====={},&&&& ,条件1的结果是：{} > 条件2的结果是：{}".format(obj1[0], num[0],obj1[0] , obj2[0],abs(obj1[0] - num[0]),abs(obj1[0] - obj2[0])))
            print("num =={}, bianma=={}".format(num,bianma))
                # print("obj1[0]==={}==obj2[0]====={}".format(obj1,obj2))

            newDictList[bianma] = oldDictList[uni1]
            # print("bianma===",bianma)
            # print("newDictList==={}=={}".format(newDictList[bianma],oldDictList[uni1]))
        return newDictList

if __name__ == "__main__":
    filename_1 = r"F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff" 
    filename_2 = r"F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file4.woff" 
    newXmlPath = r"F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/maoyan4.xml" 
    dictList = FontFaceDecode(filename_1,filename_2,newXmlPath).returnNewDict()
    print("最终结果===",dictList)