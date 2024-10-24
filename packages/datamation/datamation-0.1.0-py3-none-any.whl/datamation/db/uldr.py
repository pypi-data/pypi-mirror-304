
import gzip
import sys
import csv
import datetime as dt
import time
import locale
import subprocess
from .source import source_sql 

__all__ = ['dbuldr','dump_insert_sql','sqluldr2']

def dbuldr(conn,sql='',file = None,batch_size = 50000,fieldsep=',',rowsep='\n\r',encoding='utf-8',dbms='',included_head=True,archive =True):
    '''数据导出
    不同的数据库可能需要一些单独的方法在连接或者游标层处理一些特殊的数据类型 
    例oracle的cx_Oracle clob对象返回的并不是直接字符串 需要使用相应方法进行提取
    def OutputTypeHandler(cursor, name, defaultType, size, precision, scale):
            if defaultType == oracle.CLOB:
                return cursor.var(oracle.LONG_STRING, arraysize = cursor.arraysize)
    conn.outputtypehandler = OutputTypeHandler

    Parameters
    ------------
    conn:PEP249 API
    sql: str
        sql
    file:str
        文件名称
    batch_size:int
        批量加载行数
    delimiter:str
        字段分隔符 默认 ','
    encoding:str
        文件编码 默认utf-8
    db:str
        oracle、
        数据库类型
    archive:bool
        是否压缩文件 默认为True
    '''
    src = source_sql(conn,sql,data_format='list')
    data = []
    row_num = 0
    
    file = file if file else sql[:50]
    file = dt.datetime.now().strftime('%Y%m%d') + '_' + file

    if file.split('.')[-1] in ['GZ','gz'] or archive:
        file_obj = gzip.open
    else:
        file_obj = open

    head = src.cols
    with file_obj(file, 'wt', newline=rowsep,encoding=encoding) as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=fieldsep,lineterminator = '\r\n' ,quoting=csv.QUOTE_NONNUMERIC)
        if included_head:
            spamwriter.writerow(head)
        for n in src:
            data.append(n)
            if len(data) % batch_size == 0:
                row_num+=batch_size
                print(time.ctime(),'out row {}'.format(row_num))
                spamwriter.writerows(data)
                csvfile.flush()
                data = []
        if data:
            row_num+=len(data)
            spamwriter.writerows(data)
            print(time.ctime(),'out row {}'.format(row_num))
            data = []
    return True

def dump_insert_sql(sql,conn,table_name ='',datefunc = ''):
    '''从数据库读取数据转为insert 语句
    '''
    src = source_sql(conn,'select * from '+table_name,data_format='list')
    insert_sqls = []
    
    if datefunc:
        datefunc = datefunc +'({})'
    base_sql = f'insert into {table_name}' + '('+','.join(src.cols) +') values' 
    for row in src:
        row_values = []
        for value in row.values():
            if isinstance(value,dt.datetime):
                if datefunc:
                    row_values.append(datefunc.format(value.isoformat(sep=' ',)))
            elif value == None:
                row_values.append("null")
            elif isinstance(value,(float,int)):
                row_values.append(str(value))
            else:
                row_values.append("'{}'".format(value))
                
        insert_sqls.append(base_sql +'({})'.format(','.join(row_values)))
    return insert_sqls

def sqluldr2(user=None,query=None,sql=None,field = None,record = None,rows = None,file = None,log = None,
             fast = None,text = None,charset = None,ncharset = None,parfile = None,read = None,sort = None,hash = None,array = None,head =None,batch = None,size = None,
             serial = None,trace = None,table = None,control = None,mode = None,buffer = None,long = None,width = None,quote = None,data = None,alter = None,safe = None,
             crypt=None,sedf = None,null = None,escape = None,escf = None,format = None,exec = None,prehead = None,rowpre = None,rowsuf = None,colsep = None,presql =None,
             postsql = None,lob = None,lobdir = None,split = None,degree = None,hint = None,unique = None,update = None,parallel=None,skip = None,skipby = None,skipby2 = None,):
    '''sqluldr2 python封装
    sqluldr2是oracle的sqlldr的python封装 用于导出数据 与sqlldr的参数基本一致 但是有一些参数不支持 例如direct 、parallel

    Examples
    ---------
    sqluldr2(user='test',query='select * from test',file='test.csv',field='id,name',record='|',rows='|',head='Y',batch='Y',size=10000,mode='insert',buffer=100000,lob='Y',lobdir='lob',split='Y',degree=4,unique='id',update='name')
    '''
    kwargs = locals()
    args = []
    for k,v in kwargs.items():
        if v:
            args.append('{}={}'.format(k,v))
    if args:
        command = 'sqluldr2 ' +' '.join(args)
        return subprocess.run(command,capture_output=True,text = True)
    
