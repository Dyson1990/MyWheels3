# -*- coding:utf-8 -*-
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: sql_manager.py
    @time: 2017/3/15 14:23
    
    @info: 目前还不知道怎么改写sqlalchemy里的类，所以先不自建类了，先粗糙的满足日常需求。
    
--------------------------------
"""
import sqlalchemy
import sqlalchemy.orm
import sqlalchemy.ext.automap
import urllib.parse as urlparse

from pathlib import Path
from contextlib import closing
from loguru import logger

# =============================================================================
# # 选择数据库
# dbname_str = {
#         'oracle':"ALTER SESSION SET CURRENT_SCHEMA = \"{}\""
#         , 'mysql':"USE `{}`"
#         # , 'postgresql':"\c {}"
#         }
# =============================================================================

def __standardize_args(
        sql_args: dict
        ) -> dict:
    # 检查所需参数是否都存在，规范输入的一些参数

    if not isinstance(sql_args, dict):
        raise Exception("sql_args格式错误！！！")
    
    # 规范输入的大小写
    sql_args['db_dialect'] = sql_args['db_dialect'].lower()
    db_dialect = sql_args['db_dialect']
    
    # 兼容新旧版本
    if 'user' in sql_args and 'username' not in sql_args:
        sql_args['username'] = sql_args.pop('user')
    if 'dbname' in sql_args and 'database' not in sql_args:
        sql_args['database'] = sql_args.pop('dbname')

    # 不同的数据库，需要的参数不同
    if db_dialect == 'oracle':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'sid', 'database']

        # Oracle的数据类型比较特殊
        global np_type2sql_type,sql_type2np_type,np_type2oracle_type,oracle_type2np_type
        np_type2sql_type = np_type2oracle_type
        sql_type2np_type = oracle_type2np_type
    elif db_dialect == 'mysql':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'database']
    elif db_dialect == 'postgresql':
        needed_args = ['db_dialect', 'host', 'username', 'password', 'database']
    elif db_dialect == 'access':
        needed_args = ['db_dialect', 'file_path']

    # 缺少参数则报错，
    check_args = [s for s in needed_args if s not in sql_args]
    if check_args:
        raise Exception("缺少数据库参数：%s" % '，'.join(check_args))

    # 规定默认的参数的值 ##################################################
    sql_args['method'] = sql_args.get('method', None) # 没有参数传入，则使用fetchall
    sql_args['data_type'] = sql_args.get('data_type', 'list')
    if db_dialect == 'oracle':
        sql_args['db_driver'] = sql_args.get('db_driver', 'cx_oracle').lower()
        sql_args['port'] = sql_args.get('port', '1521')
        sql_args['query']={"sid": sql_args['sid']}
        
    elif db_dialect == 'mysql':
        sql_args['db_driver'] = sql_args.get('db_driver', 'pymysql').lower()
        sql_args['port'] = sql_args.get('port', '3306')
        sql_args['charset'] = sql_args.get('charset', 'UTF8MB4')
        """
        这种错误很有可能是SQL驱动不完整
        也可能是数据库的编码与申请的编码不符
        1366, "Incorrect string value: '\\xD6\\xD0\\xB9\\xFA\\xB1\\xEA...' for column 'VARIABLE_VALUE' at row 484")
        """
        
    elif db_dialect == 'postgresql':
        sql_args['db_driver'] = sql_args.get('db_driver', 'psycopg2').lower()
        sql_args['port'] = sql_args.get('port', '5432')

    elif db_dialect == 'access':
        sql_args['db_driver'] = sql_args.get('db_driver', 'pyodbc').lower()

        connection_string = (
            r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={sql_args.pop('file_path')};"
            r"ExtendedAnsiSQL=1;"
            )
        sql_args['query']={"odbc_connect": connection_string}
        
    #######################################################################
    return sql_args

def __sql_engine(
        sql_args: dict
        ) -> sqlalchemy.engine.base.Engine:
    
    sql_args = sql_args.copy()
    db_dialect = sql_args.pop('db_dialect')
    db_driver = sql_args.pop('db_driver')
    arg_list = ("username", "password","host","port","database","query") #URL.create()不接受其他参数 
    sql_args = {k0: v0 for k0, v0 in sql_args.items() if k0 in arg_list}
    
    conn_url = sqlalchemy.engine.URL.create(
        f"{db_dialect}+{db_driver}"
        , **sql_args
    )
    logger.info("数据库连接url为："+urlparse.unquote(conn_url.render_as_string()))
    
    return sqlalchemy.create_engine(conn_url)

def get_type_obj(
        engine: sqlalchemy.engine.base.Engine
        , type_str: str
        ) -> type:
    
    if engine.name in dir(sqlalchemy.dialects):
        base0 = getattr(sqlalchemy.dialects, engine.name).base
    else:
        logger.warning(f"{engine.name}不存在于sqlalchemy.dialects，使用了默认数据类型")
        base0 = sqlalchemy.sql.sqltypes
    
    type_dict = {s0.upper(): s0 for s0 in dir(base0)}
    return getattr(base0, type_dict[type_str.upper()], None)

def sa_base(engine: sqlalchemy.engine.base.Engine):
    metadata = sqlalchemy.schema.MetaData()
    metadata.reflect(engine, schema=engine.url.database)
    base = sqlalchemy.ext.automap.automap_base(metadata=metadata)
    base.prepare()
    
    return base

def ddl_show_tables(base):
    # return dict(base.classes)
    return base.metadata.tables
    
def table_meta(
        base: sqlalchemy.orm.decl_api.DeclarativeMeta
        , tn: str
        ) -> sqlalchemy.orm.decl_api.DeclarativeMeta:
    return getattr(base.classes, tn) # DeclarativeMeta对象

def t_cols(t_meta):
    return dict(t_meta._sa_class_manager)

def alter_table_dtype(engine, t_meta, col_name, new_type, confirm=True):
    logger.warning(f"正准备修改字段{col_name}的类型=>"+new_type)
    if confirm:
        b0 = input("是否修改(Y/n)")
    else:
        b0 = "Y"
        
    if b0 == "Y":
        with closing(engine.connect()) as conn:
            sql = f"ATLTER TABLE {t_meta.name} MODIFY COLUMN {col_name} {new_type};"
            conn.execute(sql)
    
class TableMapping():
    """待完成，没有找到一个可以直接输出表对象的方式"""
    def __init__(self, engine):
        pass

if __name__ == '__main__':
# =============================================================================
#     # 测试本地Access参数
#     sql_args = {
#         'db_dialect': 'Access'
#         , 'file_path': r'C:\Users\Weave\Desktop\BW\BW_EXPORT_202301.accdb'
#     }
#     
#     engine = __sql_engine(__standardize_args(sql_args))
#     print(get_type_obj(engine, "string"))
#     # with engine.connect() as conn:
#     #     print(conn.execute(sqlalchemy.text("SELECT top 1 * FROM export")).fetchall())
# =============================================================================
    
    # 测试本地MySQL参数
    sql_args = {
        'db_dialect': 'MySQL'
        , 'db_driver': 'pymysql'
        , "host": "192.168.1.250"
        , 'username': "Dyson"
        , "password": "1qqaq1"
        , 'dbname': 'test'
        , 'table_name': 'vote_record'
    }

        # with closing(engine.connect()) as conn:
        #     print(conn.execution_options())
    
    sql_args = __standardize_args(sql_args)
    # 使用哪种数据库，填入Oralce，MySQL等等
    engine = __sql_engine(sql_args)
    
    base = sa_base(engine)
    # print(dir(base))
    # print(type(base))
    # print(dir(base.metadata))
    # print(base.metadata.tables)
    
    t_obj = base.metadata.tables['test.employees']
    print(dir(t_obj))
    print(type(t_obj))
    # print(dir(base.metadata))
    # print(base.metadata.tables) 
    
    t_meta = dict(base.classes)['employees']
    print(dir(t_meta))
    print(type(t_meta))

    
    # t_meta = table_meta(base, "vote_record_memory")
    # print(type(t_meta))
    
    # print(type(t_meta))
    # # print(type(t_meta()))
    # print(dir(t_meta))
    # print(t_cols(t_meta))
    
    # col = t_cols(t_meta)["user_id"]
    
    # print(dir(col))
    # print(type(col))
    # print(dir(row.metadata))
    # print(col.type)
    # print(row.metadata.tables)
    
    # dtype = col.type
    # print(dir(dtype))
    # print(type(dtype))
    # print(dtype.length)
    # dtype.length = 50
    # print(dtype.length)
    
    try:
        # 初始化会话
        mk_session = sqlalchemy.orm.sessionmaker(bind=engine)
        session = mk_session()
        
        # print(dir(session))

        # 没有发生错误，则提交提交结果
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()
        
        
# =============================================================================
# from alembic.config import Config
# from alembic.command import upgrade as alembic_upgrade
# import sqlalchemy as sa
# from alembic import op
# 
# # 配置 Alembic
# alembic_cfg = Config()
# alembic_cfg.set_main_option('script_location', 'path/to/migrations')
# alembic_cfg.set_main_option('url', 'postgresql://user:password@host/dbname')
# 
# # 捕获 SQL 输出，存储到字符串变量
# sql_string = ''
# def collect_sql(stdout):
#     global sql_string
#     sql_string += stdout
# 
# def upgrade():
#     # 使用 BatchOperations.alter_column() 方法修改表格 users 的 name 列的数据类型
#     with op.batch_alter_table('users') as batch_op:
#         batch_op.alter_column('name', type_=sa.TEXT)
# 
# def downgrade():
#     # 恢复之前的数据类型
#     with op.batch_alter_table('users') as batch_op:
#         batch_op.alter_column('name', type_=sa.String(255))
# 
# # 使用 Alembic 生成 SQL 脚本
# with sa.create_engine('postgresql://user:password@host/dbname').connect() as conn:
#     trans = conn.begin()
#     try:
#         # 执行迁移操作，并输出 SQL
#         alembic_upgrade(alembic_cfg, revision='head', sql=True, stdout=collect_sql)
#         trans.commit()
# 
#         # 打印 SQL 输出
#         print(sql_string)
# 
#         # 手动执行 SQL
#         conn.execute(sql_string)
#     except:
#         trans.rollback()
#         raise
#     
# =============================================================================
# =============================================================================
# def run_sql(sql_args, sql, args=None):
#     """
#     最常用的连接MySQL的方式
#     sql 可以是一条sql语句， 也可以是sql语句组成的列表
#     :return: list
# 
#     若要转换为dataframe
#     data = [list(t) for t in data] # 要求传入列表，不能是元组
#     data = pd.DataFrame(data, columns=rp.keys())
#     """
#     data = []
# 
#     sql_args = __standardize_args(sql_args)
# 
#     try:
#         # 使用哪种数据库，填入Oralce，MySQL等等
#         engine = __sql_engine(sql_args)
# 
#         with closing(engine.connect()) as conn:
#             # 选择数据库
#             global dbname_str
#             db_dialect = sql_args['db_dialect']
#             if db_dialect in dbname_str:
#                 sql0 = sqlalchemy.text(dbname_str[db_dialect].format(sql_args['database']))
#                 conn.execute(sql0)
# 
#             # 多条SQL语句的话，循环执行
#             # rp short for ResultProxy
#             if isinstance(sql,list):
#                 for sql0 in sql:
#                     sql0 = sqlalchemy.text(sql0)
#                     rp = conn.execute(sql0)
#             elif args:
#                 sql = sqlalchemy.text(sql)
#                 rp = conn.execute(sql,args)
#             else:
#                 sql = sqlalchemy.text(sql)
#                 rp = conn.execute(sql)
# 
#             if rp is None:
#                 return None
#             data = rp.fetchall()
#             # 若要返回dataframe，使用pd.read_sql
#             return data
#     except:
#         print("数据库交互出错：\n%s" % traceback.format_exc())
#         return None
# =============================================================================
