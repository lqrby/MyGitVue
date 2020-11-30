from PIL import Image
import pytesseract
#上面都是导包，只需要下面这一行就能实现图片文字识别
# pytesseract.image_to_string
# text=pytesseract.image_to_string(Image.open(r'E:/picture/1.png'),lang='chi_sim')
# print(text)

def read_text(text_path):
    """
    传入文本(jpg、png)的绝对路径,读取文本
    :param text_path:
    :return: 文本内容
    """
    # 验证码图片转字符串
    im = Image.open(text_path)
    # 转化为8bit的黑白图片
    imgry = im.convert('L')
    # 二值化，采用阈值分割算法，threshold为分割点
    threshold = 140
    table = []
    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # 识别文本
    text = pytesseract.image_to_string(out, lang="chi_sim", config='--psm 6')
    return text
 
 
if __name__ == '__main__':
  print(read_text("E:/picture/1.png"))

