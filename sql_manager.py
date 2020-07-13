# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: sql_manager.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码，由于处于学习阶段，不打算用pandas中的read_csv、to_csv
--------------------------------
"""
import traceback

import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import sqlalchemy.dialects.oracle

import pandas as pd
import numpy as np
from contextlib import closing
import json
import random
import codecs


# log_obj = set_log.Logger('mysql_manager.log', set_log.logging.WARNING,
#                          set_log.logging.DEBUG)
# log_obj.cleanup('mysql_manager.log', if_cleanup=True)  # 是否需要在每次运行程序前清空Log文件


eng_str = {
        'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
        , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
        }
# 选择数据库
dbname_str = {
        'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
        , 'mysql':"USE `{}`"
        }
np_type2sql_type = {
        np.dtype('int64'): sqlalchemy.sql.sqltypes.Integer
        , np.dtype('float64'): sqlalchemy.sql.sqltypes.FLOAT
        , np.dtype('O'): sqlalchemy.sql.sqltypes.VARCHAR
        }
sql_type2np_type = {
        sqlalchemy.sql.sqltypes.FLOAT: np.dtype('float64')
        , sqlalchemy.sql.sqltypes.Integer: np.dtype('int64')
        , sqlalchemy.sql.sqltypes.DateTime: np.dtype('datetime64[ns]')
        , sqlalchemy.sql.sqltypes.VARCHAR: np.dtype('O')
        }
np_type2oracle_type = {
        np.dtype('int64'): sqlalchemy.dialects.oracle.base.INTEGER
        , np.dtype('float64'): sqlalchemy.dialects.oracle.base.FLOAT
        , np.dtype('O'): sqlalchemy.dialects.oracle.base.VARCHAR2
        }
oracle_type2np_type = {
        sqlalchemy.dialects.oracle.base.FLOAT: np.dtype('float64')
        , sqlalchemy.dialects.oracle.base.INTEGER: np.dtype('int64')
        , sqlalchemy.dialects.oracle.base.DATE: np.dtype('datetime64[ns]')
        , sqlalchemy.dialects.oracle.base.VARCHAR2: np.dtype('O')
        , sqlalchemy.dialects.oracle.base.NUMBER: np.dtype('float64')
        }

def run_sql(sql_args, sql, args=None):
    """
    最常用的连接MySQL的方式
    sql 可以是一条sql语句， 也可以是sql语句组成的列表
    :return: list
    
    若要转换为dataframe
    data = [list(t) for t in data] # 要求传入列表，不能是元组
    data = pd.DataFrame(data, columns=rp.keys())
    """
    data = []
    
    sql_args = __standardize_args(sql_args)

    try:
        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = __sql_engine(sql_args)
        
        with closing(engine.connect()) as conn:
            # 选择数据库
            global dbname_str
            db_dialect = sql_args['db_dialect'] 
            conn.execute(dbname_str[db_dialect].format(sql_args['dbname']))
            
            # 多条SQL语句的话，循环执行
            # rp short for ResultProxy
            if isinstance(sql,list):
                for sql0 in sql:
                    rp = conn.execute(sql0)
            elif args:
                rp = conn.execute(sql,args)
            else:
                rp = conn.execute(sql)
            
            if rp is None:
                return None
            data = rp.fetchall()
            # 若要返回dataframe，使用pd.read_sql
            return data
    except:
        print("数据库交互出错：\n%s" % traceback.format_exc())
        return None

def create_table_like_df(sql_args, args=None, **df_args):
    # 模仿dataframe的样式在数据库里建立表格
    # Column('id',Integer(),primary_key=True, autoincrement=True),
    """
    df_args中所需参数有
    table_name：数据库中的表格名称
    primary_key：需要设为主键的列名，None或缺失的话，视为不设主键
    data：dataframe表格
    size: 字段大小，缺失的话默认为20
    """
    
    # 检验所需参数是否齐全
    sql_args = __standardize_args(sql_args)
    
    table_name = df_args['table_name']
    df = df_args['data']
    size = df_args['size'] if 'size' in df_args else 20
    
    primary_key = df_args['primary_key'] if 'primary_key' in df_args else None
    
    if not isinstance(df, pd.core.frame.DataFrame):
        raise Exception('DataFrame类型错误！！！')

    try:
        # 使用哪种数据库，填入Oralce，MySQL等等
        engine = __sql_engine(sql_args)

        # 初始化元数据表格
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(engine, schema=sql_args['dbname'])
        
        # 初始化空白表格
        sql_table = sqlalchemy.Table(table_name, metadata)
        
        global np_type2sql_type
        # 为TABLE添加列映射
        for col in df.columns:
            sql_table.append_column(
                sqlalchemy.Column(
                        col,
                        np_type2sql_type[df[col].dtype](size),
                        primary_key=(col==primary_key), # 此列是不是主键
                        ),
                )
                
        # 执行建表命令
        metadata.create_all(engine)
    except:
        print("数据库交互出错：%s" % traceback.format_exc())
    
    return None

def update_df_data(sql_args, df, table_name, commit_size=None, df_to_sql=None, **col_args):
    """     
    commit_size如果是个整数，那么就将df分批插入
    分段提交有风险，第一批提交完了，第二次提交出错的话，没法回滚第一次提交的数据
    
    若col_args不为None
    col_args中必要的参数有
    df_col：输入的dataframe中，准备更新进入数据库的列
    table_col：数据库中需要更新数据的字段，相当于sql中的set后的数据
    table_keys：数据库中的筛选列，相当于sql中的where后的数据
    df_keys: 与table_keys对应的参数
    
    这时相当于
    update table_name set table_col = df_col where table_key = df_keys
    
    df_to_sql的布尔值不为False的话，就使用to_sql插入数据
    """
    if col_args:
        func = __update_df_data
    elif df_to_sql:
        func = __df_to_sql
    else:
        func = __insert_df_data
    
    if isinstance(commit_size, int):
        i = 0
        while True:
            lower0 = min(df.shape[0], i * commit_size)
            upper0 = min(df.shape[0], (i+1) * commit_size)
            print('分段上传到数据库：目前[{}, {}]'.format(lower0, upper0))
            df0 = df.iloc[lower0:upper0, :]
            if df0.empty:
                break
            func(sql_args, df0, table_name, **col_args)
    else:
        func(sql_args, df, table_name, **col_args)
    
    return None

def __insert_df_data(sql_args, df, table_name):
    # 从dataframe中将数据插入数据库
    sql_args = __standardize_args(sql_args)

    # 使用哪种数据库，填入Oralce，MySQL等等
    engine = __sql_engine(sql_args)
    try:
        # 初始化会话
        mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = mk_session()
        
        # 映射到oracle的schema中
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(engine, schema=sql_args['dbname'].lower())
        base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
        base.prepare(engine, reflect=True)
        
        df = df.rename(columns={s: s.lower() for s in df.columns})
        print(dict(base.classes.items()))
        # 创建插入数据的队列
        for i in range(df.shape[0]):
            insert_values = df.iloc[i,:].to_dict()
            item = dict(base.classes.items())[table_name.lower()](**insert_values)
            session.add(item)
            
        print('数据库插入行数：', df.shape[0])
        # 没有发生错误，则提交提交结果
        session.commit()
    except:
        session.rollback()
        raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
    finally:
        session.close()
    return None

def __df_to_sql(sql_args, df, table_name, **col_args):
    # 从dataframe中将数据插入数据库
    sql_args = __standardize_args(sql_args)

    # 使用哪种数据库，填入Oralce，MySQL等等
    engine = __sql_engine(sql_args)
    try:
        df.to_sql(table_name, engine, index=False, if_exists='append')
    except:
        raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
    return None
    
# =============================================================================
#     def 
#         """
#         相当于
#         update table_name set table_col = df_col where table_key = df_keys
#         
#         commit_size如果是个整数，那么就将df分批更新
#         分段提交有风险，第一批提交完了，第二次提交出错的话，没法回滚第一次提交的数据
#         
# 
#         """
#         if isinstance(commit_size, int):
#             i = 0
#             while True:
#                 df0 = df.iloc[i * commit_size, (i+1) * commit_size]
#                 if df0.empty:
#                     break
#                 __update_df_data(sql_args, df0, table_name, **col_args)
#         else:
#             __update_df_data(sql_args, df, table_name, **col_args)
#         
#         return None
# =============================================================================
    
def __update_df_data(sql_args, df, table_name, **col_args):

    # 规范好参数，缺少参数则报错
    if 'df_col' not in col_args \
        or 'table_col' not in col_args \
        or 'df_keys' not in col_args \
        or 'table_keys' not in col_args:
        raise Exception('df_col or table_col or table_keys not given in update_df_data')

    # 规范输入字段的大小写
    df.columns = [s.lower() for s in df.columns]
    
    table_col = col_args['table_col'].lower()
    table_keys = col_args['table_keys']
    table_keys = [s.lower() for s in table_keys] \
                 if isinstance(table_keys, list) else [table_keys.lower()]
                     
    df_col = col_args['df_col'].lower()
    df_keys = col_args['df_keys']
    df_keys = [s.lower() for s in df_keys] \
              if isinstance(df_keys, list) else [df_keys.lower()]
    
    # 检查输入数据的规范性，作为筛选字段，不能有重复值
    if df_keys:
        if df[df_keys].drop_duplicates().shape == df.shape[0]:
            raise Exception('duplicate values in update_df_data key column')
    else:
        if df.index.drop_duplicates().shape == df.shape[0]:
            raise Exception('duplicate index in update_df_data key column')
    
    table_name = table_name.lower()
    sql_args = __standardize_args(sql_args)

    # 使用哪种数据库，填入Oralce，MySQL等等
    engine = __sql_engine(sql_args)
    try:
        # 初始化事务
        mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = mk_session()
        
        # 映射到数据库中的schema
        metadata = sqlalchemy.schema.MetaData()
        metadata.reflect(engine, schema=sql_args['dbname'].lower())
        base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
        base.prepare(engine, reflect=True)
        
        # 定位到目标数据表的Python类
        table_cls = getattr(base.classes, table_name)
        
        # 将数据中的字段对象存入列表，以供检验判断等
        cls_list = [] 
        table_col_cls = getattr(table_cls, table_col) # 目标字段
        
        
        cls_list.append(table_col_cls)
        table_keys_cls = [] # 筛选字段
        for table_key in table_keys:
            table_keys_cls.append(getattr(table_cls, table_key))
            
        cls_list.extend(table_keys_cls)
        
        # 判断需要插入的数据是不是符合数据库中目标的字段的类型
        col_element_set = table_col_cls.desc().element.proxy_set.copy()
        table_col_type = col_element_set.pop().type
        if sql_type2np_type[type(table_col_type)] != df[df_col].dtype:
            s1 = type(table_col_type)
            s2 = df[df_col].dtype
            error_str = 'data type not match in update_df_data' \
                        'target column\ndb_type:{}\ndf_type:{}'.format(s1, s2)
            raise Exception(error_str)


        table_df = pd.DataFrame(session.query(*cls_list).all())
        #print(col_element_set)
                    
        # 筛选需要插入的数据
        target_df = pd.merge(df, table_df, how='left'
                              , left_on=df_keys
                              , right_on=table_keys # left_index=True, right_index=True
                              , suffixes=['', '_'])
        
        table_col_new = table_col + '_' if table_col == df_col else table_col # 应付重名时，列名的变化
        # 只更新有变化的列，避免重复更新
        target_df = target_df.loc[target_df[df_col] != target_df[table_col_new], :]
        
        # 将数据更新到数据库
        for index0 in target_df.index:
            # 逐行更新
            filter_list = [cls0 == target_df.loc[index0, cls0.name] for cls0 in table_keys_cls]
            query0 = session.query(table_cls).filter(sqlalchemy.and_(*filter_list))
            # sqlalchemy不识别pd.nan
            value0 = target_df.loc[index0, df_col]
            value0 = value0 if pd.notna(value0) else None
            
            query0.update({table_col_cls: value0}
                          , synchronize_session=False)
        
        print('数据库更新行数：', target_df.shape[0])
        # 没有发生错误，则提交提交结果
        session.commit()
    except:
        session.rollback()
        raise Exception("【insert_df_data】:fail\n{}".format(traceback.format_exc()))
    finally:
        session.close()
    return None

def __standardize_args(sql_args):
    # 检查所需参数是否都存在，规范输入的一些参数
    
    if not isinstance(sql_args, dict):
        raise Exception("sql_args格式错误！！！")
        
    # 规范输入的大小写
    sql_args['db_dialect'] = sql_args['db_dialect'].lower()
    sql_args['db_driver'] = sql_args['db_driver'].lower()
    
    # 不同的数据库，需要的参数不同
    if sql_args['db_dialect'] == 'oracle':
        needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'sid', 'dbname']
        
        # Oracle的数据类型比较特殊
        global np_type2sql_type,sql_type2np_type,np_type2oracle_type,oracle_type2np_type
        np_type2sql_type = np_type2oracle_type
        sql_type2np_type = oracle_type2np_type
        
    elif sql_args['db_dialect'] == 'mysql':
        needed_args = ['db_dialect', 'db_driver', 'host', 'user', 'password', 'dbname']
    
    # 缺少参数则报错
    check_args = [s for s in needed_args if s not in sql_args]
    if check_args:
        raise Exception("缺少数据库参数：%s" % '，'.join(check_args))
    
    # 规定默认的参数的值 ##################################################
    if 'port' not in sql_args and sql_args['db_dialect'] == 'oracle':
        sql_args['port'] = '1521'
    if 'port' not in sql_args and sql_args['db_dialect'] == 'mysql':
        sql_args['port'] = '3306'
    if 'charset' not in sql_args:
        sql_args['charset'] = 'UTF8MB4'
        """
        这种错误很有可能是SQL驱动不完整
        也可能是数据库的编码与申请的编码不符
        1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 484")
        """
    if 'method' not in sql_args:
        # 没有参数传入，则使用fetchall
        sql_args['method'] = None
    if 'data_type' not in sql_args:
        sql_args['data_type'] = 'list'
    #######################################################################
    return sql_args

def __sql_engine(sql_args):
    # 编辑salalchemy中的数据库参数字符串
    global eng_str
    db_dialect = sql_args['db_dialect']
    engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args), echo=True)
    return engine


def check_json(str0):
    try:
        json.loads(str0)
    except:
        return False
    else:
        return True

if __name__ == '__main__':    
# =============================================================================
#     # 本地测试Oracle参数
#     sql_args = {
#         'db_dialect': 'oracle'
#         , 'db_driver': 'cx_Oracle'
#         , "host": "localhost"
#         , "user": "Dyson"
#         , "password": "122321"
#         , 'sid': 'ORCL'
#         , 'dbname': 'HR'
#         , 'data_type': 'DataFrame'
#     }
#     # print(sql_manager.connect('SELECT JOB_ID, MIN_SALARY, COMMIT FROM JOBS', sql_args))
# =============================================================================
   
#    # 测试本地MySQL参数
#    sql_args = {
#        'db_dialect': 'MySQL'
#        , 'db_driver': 'pymysql'
#        , "host": "192.168.50.188"
#        , "user": "Dyson"
#        , "password": "122321"
#        , 'dbname': 'test'
#        , 'data_type': 'DataFrame'
#    }
#    df = connect(sql_args, 'SELECT * FROM `new_tzxm_infos`')
    
#    df['if_json'] = df['project_info'].apply(lambda s: check_json(s))
#    
#    print(df.loc[df['if_json']==False, 'project_code'].to_list())

    # 测试本地MySQL参数
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.50.188"
        , "user": "Dyson"
        , "password": "122321"
        , 'dbname': 'test'
        , 'data_type': 'DataFrame'
    }
    df = run_sql(sql_args, 'SELECT * FROM `new_tzxm_infos`')

    
# =============================================================================
#     df = pd.DataFrame({"job_id":{1:'{}'.format(random.randint(1,1000)), 2:'{}'.format(random.randint(1,1000))}
#                       ,"job_title":{1:'WTF',2:'WTF'}})
# =============================================================================
    #import datetime
#    df = pd.DataFrame({"JOB_ID":{1:'Daniel0', 2:'David'}
#                      , "JOB_TITLE":{1:'Faviet0', 2:'Lee'}
#                      })
                      #, "test":{1:'NEW{}'.format(random.randint(1,1000)),2:'NEW{}'.format(random.randint(1,1000))}})
#                      , "test":{1:random.randint(1,1000),2:None}})
#    print(df)
#    print(df.dtypes)
#    insert_df_data(sql_args, df, 'JOBS')
#    sql_manager.update_df_data(sql_args, df, 'JOBS'
#                               , df_col='test', table_col='test'
#                               , df_keys=['JOB_ID', "JOB_TITLE"], table_keys=['JOB_ID', "JOB_TITLE"])

