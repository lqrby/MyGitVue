import sys
sys.path.append("E:/myTestFile/TestObject/zhongfuan/yunzhangben/yzb_regression")
from case.class_api_test import ZFAclassTestCase

if __name__ == "__main__":
    app = ZFAclassTestCase()
    app.runAllCase("云账本","yzb_test_host")


# { "access_token":"", "ask_id":"",  "timestamp":"",  "sign":"" }
# [{"scope":"body","field":{"ask_id":"ask_id"}}]
# { "access_token":"", "lng":"116.359703", "id":"", "lat":"39.761146", "timestamp":"", "sign":"" }
# [{"scope":"body","field":{"seller_id":"id","lng":"lng","lat":"lat"}}]
# { "access_token":"", "pageSize":"15", "page":"1", "timestamp":"",  "sign":"" }
# { "access_token":"", "lng":"116.359703", "name":"中心", "pageSize":"15", "page":"1", "type":"1", "lat":"39.761146", "timestamp":"", "sign":"" }

	# { 
    # "native_host":"https://tyqbapi.pmm2020.com/", 
    # "api_h5":"https://tyqbapi.pmm2020.com/",
    # "quiz_h5":"https://test-quiz.pmm2020.com/",
    # "deputy_h5":"https://test-deputy.pmm2020.com/"
    # }


    #     (0, 'native'),
    #     (1, 'api_h5'),
    #     (2, 'quiz_h5'),
    #     (3, 'deputy_h5'),