#!/usr/bin/python
# -*- coding:utf-8 -*-
from mrjob.job import MRJob,MRStep

class Top3_Mean_Friends(MRJob):
    
    def mapper1(self, _,line):
        row=line.split(',')
        if row[2].isdigit() and row[3].isdigit():
            yield (row[2],int(row[3]))                      #返回年龄 和朋友个数


    def reducer1(self,age,friends):
        friends_count=list(friends)
        yield (age, sum(friends_count)/len(friends_count))  #每个年龄段的 平均朋友个数

    def mapper2(self, age,average_coun):
        yield (None,(average_coun,str(age)+'year'))

    def reducer2(self, _,average_list):                     #在平均朋友个数的基础上，求出朋友数数量最大的top3
        l=list(average_list)
        l.sort()
        top3=l[-3:]
        top3.reverse()
        for i in top3:
            yield (i[0],i[1])

    def steps(self):                                        #连接多个mapper、reducer
        return [
            MRStep(mapper=self.mapper1,reducer=self.reducer1),
            MRStep(mapper=self.mapper2,reducer=self.reducer2)
        ]

if __name__ == '__main__':
    Top3_Mean_Friends.run()

#MRStep连接多个mapper、reducer函数