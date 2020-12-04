import pymysql
#1连接数据库
def queryCursos():
    """
    youtime测试数据库地址
    """
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='ren123456',db='testcase',charset='utf8')
    #2获取游标
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor,conn