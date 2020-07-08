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

ip = "192.168.50.190"
port = "9200"

index_name = 'zhejiang_dom'

analyzer = ['DOM']
search_analyzer = ['DOM']
analyzer_type = "ik_max_word"

init_args = {
    'min_chunksize':200
    , 'insert_chunksize': 3000
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

def monitor(proc_args):
    while True:
        memory_per = psutil.virtual_memory().percent
        print('此时内存占用：', memory_per, proc_args)
        if memory_per > 85 and proc_args['insert_chunksize'] >= proc_args['min_chunksize']:
            proc_args['insert_chunksize'] = proc_args['insert_chunksize'] - 100
        else:
            proc_args['insert_chunksize'] = proc_args['insert_chunksize'] + 100
        
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
            chunk = data_gen.get_chunk(proc_args['insert_chunksize'])
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
    

    
if __name__ == "__main__":
    file_path = r'C:\Users\gooddata\Downloads\浙江DOM.csv'
    
    # 需要自定义
    ############################################################
    data_dtypes = pd.read_csv(file_path, nrows=1).dtypes
    data_gen = pd.read_csv(file_path, iterator=True)
    ############################################################
    
    proc_args = multiprocessing.Manager().dict(init_args)
    
    monitor_task = multiprocessing.Process(target=monitor, args=(proc_args,))
    monitor_task.start()
    
    # create_index(index_name, data_dtypes)
    insert_data(index_name, data_gen, proc_args)
    
    monitor_task.join()
    
    