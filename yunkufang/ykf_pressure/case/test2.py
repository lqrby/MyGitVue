from aip import AipOcr


def baiduOCR(picfile):  # picfile:图片文件名
    # 百度提供
    """ 你的 APPID AK SK """
    APP_ID = '22997234'  # 应用的appid
    API_KEY = '0pLWpT7vikvCbiKkhYbaEvzG'  # 应用的appkey
    SECRET_KEY = 'TtsQ1sLjW6aHfNNT5F8U8BuEa0PZKBQV'  # 应用的secretkey
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    i = open(picfile, 'rb')
    img = i.read()
    """ 调用通用文字识别（高精度版） """
    message = client.basicAccurate(img)
    i.close()

    # 输出文本内容
    for text in message.get('words_result'):  # 识别的内容
        # print(text)
        print(text.get('words'))


if __name__ == '__main__':
    baiduOCR('E:/picture/7.png')
    
