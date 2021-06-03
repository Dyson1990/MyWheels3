#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 14:14:37 2021

@author: wolf

原文链接：https://blog.csdn.net/zichen_ziqi/article/details/104525900/
"""

import ahocorasick
import time
 
 
class AhocorasickNer:
    def __init__(self):
        self.actree = ahocorasick.Automaton()
    
    def add_from_db(self, sql, engine):

        with engine.connect() as conn:
            resp = conn.execute(sql)
            for word, flag in resp.yield_per(1):
                self.actree.add_word(word, (flag, word))
        self.actree.make_automaton()
 
    def add_from_file(self, user_dict_path):
        flag = 0
        with open(self.user_dict_path, "r", encoding="utf-8") as file:
            for line in file:
                word, flag = line.strip(), flag + 1
                self.actree.add_word(word, (flag, word))
        self.actree.make_automaton()
 
 
    def get_ner_results(self, sentence):
        ner_results = []
        # i的形式为(index1,(index2,word))
        # index1: 提取后的结果在sentence中的末尾索引
        # index2: 提取后的结果在self.actree中的索引
        for i in self.actree.iter(sentence):
            ner_results.append((i[1], i[0] + 1 - len(i[1][1]), i[0] + 1))
        return ner_results
 
 
if __name__ == "__main__":
    import sqlalchemy
    
    eng_str = {
            'oracle':"{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{sid}?charset={charset}"
            , 'mysql': "{db_dialect}+{db_driver}://{user}:{password}@{host}:{port}/{dbname}?charset={charset}"
            }    

    sql_args = {'db_dialect': 'mysql'
                 , 'db_driver': 'pymysql'
                 , 'host': '112.124.50.195'
                 , 'user': 'root'
                 , 'password': 'hvit123!'
                 , 'dbname': 'test_lyb'
                 , 'data_type': 'DataFrame'
                 , 'charset': 'utf8'
                 , 'port': '3306'
                 , 'method': None
     }
    db_dialect = sql_args['db_dialect']
    data_engine = sqlalchemy.create_engine(eng_str[db_dialect].format(**sql_args)
                                            , execution_options={'stream_results': True}
                                            , pool_recycle=3
                                            , pool_pre_ping=True)

    ahocorasick_ner = AhocorasickNer()
    sql_str = "SELECT text, class FROM test_lyb.village_huzhou"
    ahocorasick_ner.add_from_db(sql_str, data_engine)
 
    print(ahocorasick_ner.get_ner_results('浙江省湖州市长兴县和平镇周坞山村王家自然村6号'))
    # while True:
    #     sentence = input("\nINPUT : ")
    #     ss = time.time()
    #     res = ahocorasick_ner.get_ner_results(sentence)
    #     print("TIME  : {0}ms!". format(round(1000*(time.time() - ss), 3)))
    #     print("OUTPUT:{0}".format(res))