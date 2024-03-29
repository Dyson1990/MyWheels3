#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 22:54:39 2020

@author: Administrator
"""


# # -*- coding:utf-8 -*-
from mrjob.job import MRJob
from mrjob.step import MRStep
from pathlib import Path
import traceback
import re

WORD_RE = re.compile(r"[\w']+")

class MRtest(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper0,
                   #combiner=self.combiner1,
                   reducer=self.reducer0),
            #MRStep(reducer=self.reducer2)
        ]

    def mapper1(self, _, line):
        # yield each word in the line
        for word in WORD_RE.findall(line):
            yield (word.lower(), 1)

    def combiner1(self, word, counts):
        # optimization: sum the words we've seen so far
        yield (word, sum(counts))

    def reducer1(self, word, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        # num_occurrences is so we can easily use Python's max() function.
        yield None, (sum(counts), word)

    # discard the key; it is just None
    def reducer2(self, _, word_count_pairs):
        # each item of word_count_pairs is (count, word),
        # so yielding one results in key=counts, value=word
        yield max(word_count_pairs)
        
    def mapper0(self, _,line):
        yield (None, line)
    
    def reducer0(self, _,line):
        yield (None, '\n'.join(line))


if __name__ == '__main__':
    try:
        MRtest.run()
    except:
        Path(Path(__file__).parent, 'mr_test.log')\
            .write_text(traceback.format_exc())


# =============================================================================
# 
# 
# class MRtest(MRJob):
#     
# 
#     
#     def mapper1(self, _, line):
#         '''
#         line:一行数据
#         (a,1)(b,1)(c,1)
#         (a,1)(c1)
#         (a1)
#        '''
#         pattern=re.compile(r'(\W+)')
#         for word in re.split(pattern=pattern,string=line):
#             if word.isalpha():
#                 yield (word.lower(),1)
# 
# 
#     def reducer1(self, word, count):
#         #shuff and sort 之后
#         '''
#         (a,[1,1,1])
#         (b,[1])
#         (c,[1])
#         '''
#         l=list(count)
#         yield (word,sum(l))
#         
#         
#     def mapper2(self, age,average_coun):
#         pass
# 
#     def reducer2(self, _,average_list):        
#         pass
# 
#     def steps(self):                 
#         return [
#             MRStep(mapper=self.mapper1,reducer=self.reducer1),
#             #MRStep(mapper=self.mapper2,reducer=self.reducer2)
#         ]
# 
# if __name__ == '__main__':
#     try:
#         MRtest.run()
#     except:
#         Path(Path(__file__).parent, 'mr_test.log')\
#             .write_text(traceback.format_exc())
# =============================================================================
