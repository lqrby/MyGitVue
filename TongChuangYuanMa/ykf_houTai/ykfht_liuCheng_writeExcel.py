
import sys
<<<<<<< HEAD
sys.path.append("E:/myTestFile/TestObject/TongChuangYuanMa")
=======
sys.path.append("F:/myTestFile/TestObject/TongChuangYuanMa")
>>>>>>> cab62fe0f6e06f77d99222bd0a09668caebc2748
# from Interface.QueryUsers import queryUsers
# from test_script.publicscript.publicRequestMethod import PublicRequest
from excel_group import ExcelGroup




def liuCheng():
    file_path = "C:/Users/renbaoyu/Desktop/8.21录单.xlsx"
    filepath2 = "C:/Users/renbaoyu/Desktop/ludan.txt"
    excelList = ExcelGroup.readExcel(file_path) #获取excel
    print(excelList)
    if excelList:
        groupList = ExcelGroup.merge_dict(excelList)  #对表格数据分组
        print("groupList=====",groupList)
        if groupList:
            print("777")
            ExcelGroup.writeText(filepath2,groupList)
            print("*******************")


if __name__ == "__main__":
    
    liuCheng()        
        
