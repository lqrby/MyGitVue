title = "我们投资还要交易，你测试下好吗"
name_list = ["投资", "交易", "测试"]
for name in name_list:
    if name in title:
        title = title.replace(name,"")
        print("title====={}".format(title))

print("wode title====={}".format(title))