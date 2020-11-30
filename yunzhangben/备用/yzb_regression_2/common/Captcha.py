import redis
import re
def returnCaptcha(token):
    """
    redis缓存数据库连接
    """

    # 连接池
    pool = redis.ConnectionPool(host="172.20.100.27", port=6379,password="time25@Cs.redis",max_connections=1024)
    conn = redis.Redis(connection_pool=pool)
    # print("666",conn.get("yt:users:sms:code:zc{}".format("token")))
    # token = "yk_0002cf7687daa0d62cd778e7aca7db41"
    # print("token = {}".format(token))
    
    bytescode = conn.get("yt:users:sms:code:zc{}".format(token))
    # print("类型：",type(bytescode))
    strcode = str(bytescode, encoding = "utf-8")  
    code = re.findall(r'\d{4}',strcode)[0]
    
    # code = re.compile(r'\d{4}').search(strcode).group(1)
    return code
    

