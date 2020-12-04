from fontTools.ttLib import TTFont



filename = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file2.woff"

font = TTFont(filename)
# obj_list1=font.getGlyphNames()[1:-1]   #获取所有字符的对象，去除第一个和最后一个
# uni_list1=font.getGlyphOrder()[2:]    #获取所有编码，去除前2个
# print("obj_list1====={}".format(obj_list1))
# print("uni_list1====={}".format(uni_list1))
# # font.saveXML('F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/maoyan2.xml')
font_map = font['cmap'].getBestCmap()
# print(font_map)
# # kv = font.keys()
d = {
"x":".",
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
for key in font_map:
    font_map[key] = d[font_map[key]]
print(font_map)
