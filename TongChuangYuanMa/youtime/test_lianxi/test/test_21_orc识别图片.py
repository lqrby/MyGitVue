
import pytesseract

from PIL import Image


piclist = "C:/Users/renbaoyu/Desktop/aaa/2.png"

image = Image.open(piclist)

code = pytesseract.image_to_string(image,lang='chi_sim')

# target = open(str(piclist)+'output.txt', 'w')

# target.write(str(code)+'\n')

print(code)

# target.close()




  
