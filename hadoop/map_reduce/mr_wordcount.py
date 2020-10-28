#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:54:39 2020

@author: Administrator

python3 mr_sample.py -r hadoop hdfs://192.168.0.116:9000/tmp/test/Alice.txt
"""

from mrjob.job import MRJob
import re
from pathlib import Path

file_dir = Path(__file__).parent

class MRwordCount(MRJob):

    
    def mapper(self, _, line):
        '''
        line:一行数据
        (a,1)(b,1)(c,1)
        (a,1)(c1)
        (a1)
       '''
        pattern=re.compile(r'(\W+)')
        for word in re.split(pattern=pattern,string=line):
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
        yield (word,sum(l))

if __name__ == '__main__':
    MRwordCount.run() #run()方法，开始执行MapReduce任务。

