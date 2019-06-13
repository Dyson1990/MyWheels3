# -*- coding: utf-8 -*-
# /usr/bin/python3
"""
--------------------------------
Created on %(date)s
@author: Dyson
--------------------------------
"""
import os
import sys
import pandas as pd
import numpy as np
import pymongo
import json
import codecs


def __standardize_args(engine_args):
    # 检查所需参数是否都存在，规范输入的一些参数
    if not isinstance(engine_args, dict):
        raise Exception("engine_args格式错误！！！")
    needed_args = ['host', 'dbname']
    
    if set(needed_args).difference(set(engine_args)):
        raise Exception("缺少数据库参数")
        
    if 'port' not in engine_args:
        engine_args['port'] = '27017'
    
def __engine(engine_args):
    """
    创建与MongoDB的连接
    """
    __standardize_args(engine_args)
    
    host = engine_args['host']
    port = int(engine_args['port'])
    user = engine_args['user'] if 'user' in engine_args else None
    password = engine_args['password'] if 'password' in engine_args else None
    role = engine_args['role'] if 'role' in engine_args else engine_args['dbname']
    engine = pymongo.MongoClient("mongodb://{}:{}/".format(host, port))
    
    if all([user, password]):
        role = getattr(engine, role)
        role.authenticate(user, password, mechanism='SCRAM-SHA-1') 
    return engine

def create_collection(collection_name, engine_args):
    """
    创建集合
    
    注意: 在 MongoDB 中，集合只有在内容插入后才会创建! 
    就是说，创建集合(数据表)后要再插入一个文档(记录)，集合才会真正创建。
    """
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    
    db[collection_name] #不需要返回值
    return None

def drop_collection(collection_name, engine_args):
    """
    删除集合
    """
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    if collection_name in db.list_collection_names():
        collection = db[collection_name]
        collection.drop()
        print('mongodb_manager[drop_collection] => \n{} dropped'.format(collection_name))
    else:
        print('mongodb_manager[drop_collection] =>'
              '\nWarning: {} is not in database list!!!'.format(collection_name))
    return None
    
def insert_doc(doc_list, collection_name, engine_args, load_json=None):
    """
    向集合插入数据
    """
    # 支持传入DataFrame
    if isinstance(doc_list, pd.core.frame.DataFrame):
        load_json_func = lambda ser:ser.apply(__load_json)
        if isinstance(load_json, list) and bool(load_json):
            doc_list.loc[:, list] = doc_list.loc[:, list].apply(load_json_func
                                                                , axis=1)
        elif load_json == 'auto':
            doc_list = doc_list.apply(load_json_func, axis=1)
            
        doc_list = doc_list.to_dict(orient = 'records')
        
    if not isinstance(doc_list, list): 
        raise Exception("doc_list应为类似于[dict, dict......]的列表结构")
        
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    
    collection = db[collection_name]
    resp = collection.insert_many(doc_list)
    print('mongodb_manager[insert_doc] '
          '=> \naffected rows: {}'.format(len(resp.inserted_ids)))
    return None

def delete_doc(filter_dict, collection_name, engine_args, method='regex'):
    """
    从集合中删除数据
    """
    if not isinstance(filter_dict, dict): 
        raise Exception("筛选对象filter_dict应为字典结构")
    
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    
    collection = db[collection_name]
    if method == 'regex':
        # 此处的filter_dict应该为类似{ "name": {"$regex": "^F"} }的正则表达式字典
        resp = collection.delete_many(filter_dict) 
    else:
        # 此处的filter_dict应该为类似{ "name": "Taobao" }的精确的字段名
        resp = collection.delete_one(filter_dict)
        
    print('mongodb_manager[delete_doc] '
          '=> \naffected rows: {}'.format(len(resp.inserted_ids)))        
    return None

def update_doc(filter_dict, update_dict, collection_name, engine_args, method='regex'):
    """
    在集合中更新数据
    """
    if not isinstance(filter_dict, dict): 
        raise Exception("筛选对象filter_dict应为字典结构")
    if not isinstance(update_dict, dict) or '$set' not in update_dict: 
        raise Exception("更新对象filter_dict应为类似"\
                        "{\"$set\": {\"alexa\": \"123\" } }字典结构")
    
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    
    collection = db[collection_name]
    if method == 'regex':
        # 此处的filter_dict应该为类似{ "name": {"$regex": "^F"} }的正则表达式字典
        resp = collection.update_many(filter_dict, update_dict)
        print('mongodb_manager ==> '\
              'update_doc affected rows: {}'.format(len(resp.inserted_ids)))
    else:
        # 此处的filter_dict应该为类似{ "name": "Taobao" }的精确的字段名
        resp = collection.update_one(filter_dict, update_dict)
        print('mongodb_manager ==> '\
              'update_doc affected rows: {}'.format(len(resp.inserted_ids)))
        
    return None

def select_doc(filter_dict, collection_name, engine_args, method='regex'):
    if not isinstance(filter_dict, dict) or filter_dict: 
        raise Exception("筛选对象filter_dict应为字典结构")
    
    engine = __engine(engine_args)
    dbname = engine_args['dbname']
    db = engine[dbname]
    
    collection = db[collection_name]
    if bool(filter_dict):
        pass
    else:
        return tuple(collection.find())
    
def __load_json(s):
    try:
        return json.loads(s)
    except:
        return s
    
        
if __name__ == '__main__':
#    df = pd.DataFrame(np.random.rand(100,100))
#    df.columns = ['c' + str(i) for i in df.columns]
#    with codecs.open(r'C:\Users\gooddata\Desktop\json样本数据.csv', 'r', 'utf-8') as f:
#        df = pd.read_csv(f)
    engine_args = {'host': 'localhost'
                   , 'dbname': 'test_db'
                   , 'port': '27017'
                   }
#    insert_doc(df, 'json_collection', engine_args)
#    create_collection('json_collection', engine_args)
#    insert_doc(df, 'json_collection', engine_args, load_json='auto')

    json_data = select_doc({}, 'data_2017', engine_args)
    df = pd.DataFrame(json_data, dtype=np.object)
    df['_id'] = df['_id'].astype(np.str)
#    res = df.to_dict(orient = 'records')
    print(df)
    
#    with codecs.open(r'C:\Users\gooddata\Desktop\tzxm_infos.json', 'w', 'utf-8') as f:
#        json.dump(res, f, ensure_ascii=False, indent=2)
        
        
        
        
        
        