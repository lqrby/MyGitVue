import hashlib
data = 'ren123456'
cipher = hashlib.md5(data.encode()).hexdigest()
print(cipher)