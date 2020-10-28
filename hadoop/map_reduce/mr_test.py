#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:54:39 2020

@author: Administrator
"""


# # -*- coding:utf-8 -*-
from mrjob.job import MRJob,MRStep
from pathlib import Path
import traceback

class MRtest(MRJob):
    
    def mapper0(self, _,line):
        yield (None, line)
    
    def reducer0(self, _,line):
        yield (None, '\n'.join(line))
    
    def mapper1(self, _,line):
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


    def reducer1(self, word, count):
        #shuff and sort 之后
        '''
        (a,[1,1,1])
        (b,[1])
        (c,[1])
        '''
        l=list(count)
        yield (word,sum(l))
        
        
    def mapper2(self, age,average_coun):
        pass

    def reducer2(self, _,average_list):        
        pass

    def steps(self):                 
        return [
            MRStep(mapper=self.mapper1,reducer=self.reducer1),
            #MRStep(mapper=self.mapper2,reducer=self.reducer2)
        ]

if __name__ == '__main__':
    try:
        MRtest.run()
    except:
        Path(Path(__file__).parent, 'mr_test.log')\
            .write_text(traceback.format_exc())