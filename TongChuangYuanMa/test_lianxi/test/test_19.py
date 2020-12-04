from fontTools.ttLib import TTFont



filename = "F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/file3.woff"

font = TTFont(filename)
font.saveXML('F:/myTestFile/TestObject/TongChuangYuanMa/txt_file/maoyan3.xml')
# font_map = font['cmap'].getBestCmap()
# print(font_map)
# # kv = font.keys()
# d = {
# "x":".",
#  "uniE80C":"4",
#  "uniE836":"7", 
#  "uniE8E7":"6",
#  "uniEEEC":"3", 
#  "uniEF1B":"0", 
#  "uniF104":"2", 
#  "uniF424":"5", 
#  "uniF487":"1", 
#  "uniF4AE":"9", 
#  "uniF534":"8"
# }
# for key in font_map:
#     font_map[key] = d[font_map[key]]
# print(font_map)
