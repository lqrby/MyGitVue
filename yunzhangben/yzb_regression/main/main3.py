import sys
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
from case.ykf_api_test import ClassTestCase_yzb


if __name__ == "__main__":
    app = ClassTestCase_yzb()
    app.runAllCase("云库房","ykf_test_host")


# { "access_token":"", "ask_id":"",  "timestamp":"",  "sign":"" }
# [{"scope":"body","field":{"ask_id":"ask_id"}}]
# { "access_token":"", "lng":"116.359703", "id":"", "lat":"39.761146", "timestamp":"", "sign":"" }
# [{"scope":"body","field":{"seller_id":"id","lng":"lng","lat":"lat"}}]
# { "access_token":"", "pageSize":"15", "page":"1", "timestamp":"",  "sign":"" }
# { "access_token":"", "lng":"116.359703", "name":"中心", "pageSize":"15", "page":"1", "type":"1", "lat":"39.761146", "timestamp":"", "sign":"" }

    