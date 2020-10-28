#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:54:39 2020

@author: Administrator

python3 mr_sample.py -r hadoop hdfs://192.168.0.116:9000//tmp/test/Alice.txt
"""
import traceback
import codecs
from mrjob.job import MRJob
import re
from pathlib import Path

file_dir = Path(__file__).parent

class MRwordCount(MRJob):
    '''
        line:一行数据
        (a,1)(b,1)(c,1)
        (a,1)(c1)
        (a1)
       '''
    def mapper(self, _, line):
        pattern=re.compile(r'(\W+)')
        for word in re.split(pattern=pattern,string=line):
            file_path = Path(file_dir, 'mr_sample_mapper.log').as_posix()
            with codecs.open(file_path, 'a', 'utf-8') as fp:
                fp.write(line)
            if word.isalpha():
                yield (word.lower(),1)


    def reducer(self, word, count):
        #shuff and sort 之后
        '''
        (a,[1,1,1])
        (b,[1])
        (c,[1])
        '''
        l=list(count)
        # with codecs.open('mr_sample_mapper.log', 'a', 'utf-8') as fp:
        #     fp.write(word, count)
        yield (word,sum(l))

if __name__ == '__main__':
    MRwordCount.run() #run()方法，开始执行MapReduce任务。

# =============================================================================
# from mrjob.job import MRJob
# 
# class  WordCount(MRJob):
# 
#     def  mapper(self,key,lines):
#         line =lines.strip().split(' ')
# 
#         for word in line:
#             yield  word,1
# 
#     def  reduceer(self,words,occrrence):
#         yield  words,sum(occrrence)
# 
# 
# if __name__ =="__main__":
#     try:
#         WordCount.run()
#     except:
#         with codecs.open('mr_sample.log', 'w', 'utf-8') as fp:
#             fp.write(traceback.format_exc())
# =============================================================================
