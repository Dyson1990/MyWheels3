#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 13:39:23 2021

@author: wolf
原文链接：https://blog.csdn.net/shaoqiangaa/article/details/110632185
"""


'''
判断一条语句是否包含词库中的词
'''

class Searching:
    def __inif__(self, word_list):
        '''包含关系方法所需的词典'''
        self.word_set = set(word_list)
        self.num_list = [len(word) for word in self.word_set if len(word)>0]#词库字数
        self.num_list = list(set(self.num_list))#词库字数去重[2,3,4]
    
    def slice_len(self, s,n):
        '''截取字符串中固定长度的所有词'''
        result_list = []
        length = len(s)
        for i in range(0,length):
            if i < length-n+1:
                result_list.append(s[i:i+n])
        return result_list
    
    def mycon(self, s,word_list):
        '''词库可能字数的词全部切分且与词库比较'''
        temp_list = []#所有切分词
        for num in self.num_list:
            temp_list.extend(self.slice_len(s,num))
        temp_list1 = list(set(temp_list) & self.word_set)#求交集
        return sorted(temp_list1,key=len,reverse=True)
    
if __name__ == '__main__':
    pass    