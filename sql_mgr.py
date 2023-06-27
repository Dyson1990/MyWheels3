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
import importlib.util

from contextlib import closing
from loguru import logger
from pathlib import Path
py_dir = Path(__file__).parent

try:
    # 从同级文件夹里读取db_cfg.py
    spec = importlib.util.spec_from_file_location("db_cfg", py_dir/"db_cfg.py")
    db_cfg = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db_cfg)
except Exception as e0:
    # 从github读取db_cfg.py
    import requests
    import types
    import sys
    owner = "Dyson1990"
    repo = "MyWheels3"
    branch = "master"
    module_p = "db_cfg.py"
    # 从GitHub API获取源代码并打包成字节码
    url = f'https://api.github.com/repos/{owner}/{repo}/contents/{module_p}'
    params = {'ref': branch} if branch else None
    headers = {'Accept': 'application/vnd.github.v3.raw'}
    proxies = {'http': 'socks5://127.0.0.1:10808', 'https': 'socks5://127.0.0.1:10808'}
    response = requests.get(url,params=params,headers=headers,proxies=proxies)
    source_code_raw = response.text
    spec = importlib.util.spec_from_loader("db_cfg", loader=None, origin="<string>")
    db_cfg = types.ModuleType(spec.name)
    exec(source_code_raw, db_cfg.__dict__)
    sys.modules[spec.name] = db_cfg
    globals()[spec.name] = db_cfg
    logger.info(f"downloaded db_cfg.py from web, error: {e0}")

def __sql_engine(
        cfg: db_cfg.DBConfig
        ) -> sqlalchemy.engine.base.Engine:
    drivername = cfg.pop('drivername')
    arg_list = ("username", "password","host","port","database","query") #URL.create()不接受其他参数 
    sql_args = {k0: v0 for k0, v0 in cfg.items() if k0 in arg_list}
    
    conn_url = sqlalchemy.engine.URL.create(
        drivername
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
        , "host": "192.168.1.190"
        , 'username': "Dyson"
        , "password": "1qqaq1"
        , 'dbname': 'test'
        , 'table_name': 'vote_record'
    }

        # with closing(engine.connect()) as conn:
        #     print(conn.execution_options())
        
    cfg = db_cfg.DBConfig('MySQL', **sql_args)
    
    # 使用哪种数据库，填入Oralce，MySQL等等
    engine = __sql_engine(cfg)
    
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
