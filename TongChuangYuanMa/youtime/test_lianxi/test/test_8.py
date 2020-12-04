
# -*- coding: utf-8 -*-
import base64

def safe_base64_decode(s):
   str=s.decode()
#    str=s.decode('utf-8','ignore')
   strok = str.replace("=","") 
   mybytes =strok.encode('UTF-8') 
   print("------------:",mybytes )
   return mybytes
if __name__ == "__main__":
    assert b'YWJjZA'== safe_base64_decode(b'YWJjZA=='), safe_base64_decode('YWJjZA==')
    # assert b'abcd' == safe_base64_decode(b'YWJjZA')#, safe_base64_decode('YWJjZA')
    print('ok')