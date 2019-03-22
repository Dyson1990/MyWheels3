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

class mongodb_manager(object):

    def __init__(self):
        pass
    
    def __standardize_args(self, engine_args):
        # 检查所需参数是否都存在，规范输入的一些参数
        if not isinstance(engine_args, dict):
            raise Exception("engine_args格式错误！！！")
        needed_args = ['host', 'user', 'password', 'dbname']
        
        if not set(needed_args).difference(set(engine_args)):
            raise Exception("缺少数据库参数")
            
        if 'port' not in engine_args:
            engine_args['port'] = '27017'
        
    def __sql_engine(self, engine_args):
        host = engine_args['host']
        port = engine_args['port']
        engine = pymongo.MongoClient("mongodb://{}:{}/".format(host, port))
        
        return engine
    
    def create_collection(self, collection_name, engine_args):
        # 创建集合
        engine = self.__sql_engine(engine_args)
        dbname = engine_args['dbname']
        db = engine[dbname]
        
        db[collection_name] #不需要返回值
        return None
    
    def drop_collection(self, collection_name, engine_args):
        # 创建集合
        engine = self.__sql_engine(engine_args)
        dbname = engine_args['dbname']
        db = engine[dbname]
        
        db.drop()
        
        return None
        
    def insert_doc(self, doc_list, collection_name, engine_args):
        """
        向集合插入数据
        """
        # 支持传入DataFrame
        if isinstance(doc_list, pd.core.frame.DataFrame): 
            doc_list = doc_list.to_dict(orient = 'records')
            
        if not isinstance(doc_list, list): 
            raise Exception("data_dict应为类似于[dict, dict......]的列表结构")
            
        engine = self.__sql_engine(engine_args)
        dbname = engine_args['dbname']
        db = engine[dbname]
        
        collection = db[collection_name]
        resp = collection.insert_many(doc_list)
        print('mongodb_manager ==> '\
              'insert_doc affected rows: {}'.format(len(resp.inserted_ids)))
        return None
    
    def delete_doc(self, filter_dict, collection_name, engine_args, method='regex'):
        if not isinstance(filter_dict, dict): 
            raise Exception("筛选对象filter_dict应为字典结构")
        
        engine = self.__sql_engine(engine_args)
        dbname = engine_args['dbname']
        db = engine[dbname]
        
        collection = db[collection_name]
        if method == 'regex':
            # 此处的filter_dict应该为类似{ "name": {"$regex": "^F"} }的正则表达式字典
            resp = collection.delete_many(filter_dict)
            print('mongodb_manager ==> '\
                  'delete_doc affected rows: {}'.format(len(resp.inserted_ids)))
        else:
            # 此处的filter_dict应该为类似{ "name": "Taobao" }的精确的字段名
            resp = collection.delete_one(filter_dict)
            print('mongodb_manager ==>'\
                  ' delete_doc affected rows: {}'.format(len(resp.inserted_ids)))
            
        return None
    
    def update_doc(self, filter_dict, update_dict, collection_name, engine_args, method='regex'):
        if not isinstance(filter_dict, dict): 
            raise Exception("筛选对象filter_dict应为字典结构")
        if not isinstance(update_dict, dict) or '$set' not in update_dict: 
            raise Exception("更新对象filter_dict应为类似"\
                            "{\"$set\": {\"alexa\": \"123\" } }字典结构")
        
        engine = self.__sql_engine(engine_args)
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
    
    def select_doc(self, filter_dict, collection_name, engine_args, method='regex'):
        if not isinstance(filter_dict, dict) or filter_dict: 
            raise Exception("筛选对象filter_dict应为字典结构")
        
        engine = self.__sql_engine(engine_args)
        dbname = engine_args['dbname']
        db = engine[dbname]
        
        return None
        
if __name__ == '__main__':
    mongodb_manager = mongodb_manager()
    df = pd.DataFrame(np.random.rand(100,100))
    df.columns = ['c' + str(i) for i in df.columns]
    engine_args = {
            'host': 'localhost'
            , 'dbname': 'test_db'
            , 'port': '27017'
            }
    mongodb_manager.insert_data(df, 'test_insert', engine_args)
        
        
        
        
        
        