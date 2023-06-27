#encoding=utf-8
import pandas as pd
import numpy as np
import elasticsearch
import elasticsearch.helpers
import multiprocessing
import psutil
import time
import datetime
import hashlib
import math
import time
import os

ip = "192.168.50.190"
port = "9200"

index_name = 'zhejiang_dom'

analyzer = ['DOM']
search_analyzer = ['DOM']
analyzer_type = "ik_max_word"

init_args = {
    'min_chunksize':200
    , 'cur_chunksize': 3000
    , 'trigger': True
    }

np_dtype2es_type = {
    np.dtype('O'): 'text'
    , np.dtype('int64'): 'integer'
    # , np.dtype.str: 'text'
    # , np.dtype.int: 'integer'
    # , np.dtype.float: 'float'
    }


es = elasticsearch.Elasticsearch(['{}:{}'.format(ip, port)])

# 检查elasticsearch状态
# es.cluster.health(wait_for_status='yellow', request_timeout=1)

def mer_monitor(proc_args):
    while True:
        memory_per = psutil.virtual_memory().percent
        print('此时内存占用：', memory_per)
        if memory_per > 85 and proc_args['cur_chunksize'] >= proc_args['min_chunksize']:
            proc_args['cur_chunksize'] = proc_args['cur_chunksize'] - 100
        else:
            proc_args['cur_chunksize'] = proc_args['cur_chunksize'] + 100
            
        if not proc_args['trigger']:
            break
        
        time.sleep(10)
        
def res_monitor(args):
    save_path = 'es_test.csv'
    
    res_list = args['res_list']
    lock = args['proc_lock']
    proc_args = args['proc_args']
    while True:
        if len(res_list) > 10000 or not proc_args['trigger']:
            output = pd.DataFrame(list(res_list))
            with lock:
                output.to_csv(save_path
                              , index=False
                              , mode='a'
                              , encoding='utf_8_sig'
                              )
            del res_list
            res_list = multiprocessing.Manager().list()
                
        if len(res_list) == 0 and not proc_args['trigger']:
            break
        
        time.sleep(10)
    
    
    

def create_index(index_name, data_dtypes):
    global np_dtype2es_type, es
    
    
    body = {
        "mappings": {
            "properties": {
                col:{
                    "type": np_dtype2es_type[data_dtypes[col]],
                    "analyzer": analyzer_type if col in analyzer else None,
                    "search_analyzer": analyzer_type if col in search_analyzer else None,
                } for col in data_dtypes.index}
        }
    }
    
    es.indices.create(index=index_name, body=body)
    
def insert_data(index_name, data_gen, proc_args):
    """
    data_gen仅接受iterator，节约内存
    """
    global es
    
    print(es.cluster.health(wait_for_status='yellow', request_timeout=1))
    
    while True:
        try:
            chunk = data_gen.get_chunk(proc_args['cur_chunksize'])
        except StopIteration:
            break
            
        chunk = chunk.astype(np.str)
        action = ({"_index": index_name
                   ,"_id": hashlib.md5('-'.join([str(e) for e in d0.values()]).encode('utf-8')).hexdigest()
                   ,"_source": d0}
                  for d0 in chunk.to_dict(orient='record')
                  )
        elasticsearch.helpers.bulk(es, action)
        print(datetime.datetime.now(), '上传成功')
        
def search_data(args):
    """
    """
    global ip, port, index_name
    
    str_list = args['data']
    res_list = args['res_list']
    start_time = time.time()
    
    es = elasticsearch.Elasticsearch(['{}:{}'.format(ip, port)])

    
    for str0 in str_list:
        search_str = {"query": {
                        "bool": {
                          "must": [
                            {
                              "match": {
                                "DOM": str0
                              }
                            }
                          ]
                        }
                      }
                    }
        res = es.search(index=index_name, body=search_str)
        res = res['hits']['hits']
        
        for d0 in res:
            l0 = [
                  ['_str',str0]
                  ,['_id',d0['_id']]
                  ,['_score',d0['_score']]
                  ]
            l0 = l0 + list(d0['_source'].items())
            res_list.append(dict(l0))
    print('进程：', os.getpid(), '查询次数：', len(str_list), '耗时：', time.time()-start_time)

    
if __name__ == "__main__":
    file_path = r'C:\Users\gooddata\Downloads\浙江DOM.csv'
    
    # 需要自定义
    ############################################################
    data_dtypes = pd.read_csv(file_path, nrows=1).dtypes
    data_gen = pd.read_csv(file_path, iterator=True)
    ############################################################
    
    proc_args = multiprocessing.Manager().dict(init_args)
    proc_lock = multiprocessing.Manager().Lock()
    res_list = multiprocessing.Manager().list()
    
    monitor_task_list = []
    monitor_task_list.append(multiprocessing.Process(target=mer_monitor
                                                     , args=(proc_args,))
                             )
    
    args = {'res_list': res_list, "proc_lock": proc_lock, "proc_args": proc_args}
    monitor_task_list.append(multiprocessing.Process(target=res_monitor
                                                     , args=(args,))
                             )
    
    for monitor_task in monitor_task_list:
        monitor_task.start()
    
# =============================================================================
#     create_index(index_name, data_dtypes)
# =============================================================================
    
# =============================================================================
#     insert_data(index_name, data_gen, proc_args)
# =============================================================================
    
    proc_count = 6
    data_list = data_gen.get_chunk(1000)['DOM'].dropna().tolist()
    step = math.ceil(len(data_list)/proc_count)
    task_list = []
    start_time = time.time()
    print(datetime.datetime.now(), '开始建立搜索进程')
    for i in range(6):
        args = {"data": data_list[0:step]
                , "proc_lock": proc_lock
                , "proc_args": proc_args
                , "res_list": res_list
                }
        task = multiprocessing.Process(target=search_data, args=(args,))
        data_list = data_list[step:]
        
        task_list.append(task)
    
    print(datetime.datetime.now(), '启动进程')
    for task in task_list:
        task.start()
        
    for task in task_list:
        task.join()
    
    proc_args['trigger'] = False
    
    for monitor_task in monitor_task_list:
        monitor_task.join()
    
    print(datetime.datetime.now(), 'elasticsearch搜索结束，耗时：', time.time()-start_time)
    
    
    
