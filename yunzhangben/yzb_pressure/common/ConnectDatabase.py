import pymysql
#1连接数据库
def queryCursos():
    """
    youtime测试数据库地址
    """
    conn=pymysql.connect(host='172.20.100.26',port=3306,user='time',password='time25!QAZ',db='db_timebank',charset='utf8')
    #2获取游标
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor,conn

def queryCursos_ykf():
    """
    云库房预发布数据库地址
    """
    conn=pymysql.connect(host='39.96.21.78',port=3306,user='db_pressure_test',password='mhkSz4Fh3lwSLcW',db='db_518aic_test',charset='utf8')
    #2获取游标
    # cursor = conn.cursor()
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor,conn


def queryCursos_local():
    """
    本地数据库地址
    """
    conn=pymysql.connect(host='127.0.0.1',port=3306,user='root',password='ren123456',db='testcase',charset='utf8')
    #2获取游标
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    return cursor,conn