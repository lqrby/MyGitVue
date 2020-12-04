from .ConnectDatabase import queryCursos_ykf,queryCursos

def queryUsers(start_num=30,number=10):
    '''
    #3执行查询，并获取查询的用户总行数
    '''
    cursor,conn = queryCursos()
    print(start_num,number)
    rowNums = cursor.execute('SELECT id,nickname,mobile FROM tb_user limit {},{}'.format(start_num,number))
    print('查询的行数为' + str(rowNums))
    #4.遍历结果，获取查询的结果
    ResultList = cursor.fetchall()
    for i in range(len(ResultList)):
        print(ResultList[i])
    #提交如果需要插入语句的时候使用commit
    #conn.commit()
    #关闭
    cursor.close()
    conn.close()
    return ResultList


def queryUsers_ykf(start_num=30,number=10):
    '''
    #云库房执行查询，并获取查询的用户总行数
    '''
    cursor,conn = queryCursos_ykf()
    print(start_num,number)
    rowNums = cursor.execute('SELECT password_hash,mobile FROM user order by "mobile" desc limit {},{}'.format(start_num,number))
    print('查询的行数为' + str(rowNums))
    #4.遍历结果，获取查询的结果
    ResultList = cursor.fetchall()
    for i in range(len(ResultList)):
        print(ResultList[i])
    #提交如果需要插入语句的时候使用commit
    #conn.commit()
    #关闭
    cursor.close()
    conn.close()
    return ResultList
