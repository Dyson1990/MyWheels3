# -*- coding:utf-8 -*-

"""
@author: Dyson
@software: PyCharm Community Edition
@file: csv_report.py
@time: 2016/7/28 17:46
@info: 个人常用代码
"""

import csv
import codecs
import os

class csv_report():
    
    def __init__(self):
        pass
        
    def output_data(self, data, file_name, title = [], path = os.getcwd(), method = 'wb'):
        csvfile = file('%s\\%s.csv' %(path, file_name), method)
        print u"【csv_report】输出位置为%s\\%s.csv" %(path, file_name)
        csvfile.write(codecs.BOM_UTF8)  # 防止乱码
        writer = csv.writer(csvfile)

        if type(data) == type({}):
            """
            data => {key1:data_list1,key2:data_list2,............} 情况1
                    {key1:str,key2:str,............} 情况2
            title => list
            """
            print 'csv_report.py => ', type(data)
            for key in data:
                data_tmp = data[key]

                if not data_tmp:
                    print u"【csv_report】关键词'%s'应对数据为空" % key
                    continue
                #情况2

                if type(data_tmp) != type([]) and type(data_tmp) != type(()):
                    data_tmp = [data_tmp,]

                writer.writerow([key,]) # 数据总标题，必须输入列表，防止文字分裂
                
                writer.writerow(title)

                if type(data_tmp[0]) == type([]) or type(data_tmp[0]) == type(()): # 区分[xx,xx,xx...]和[[xx,xx..], [xx,xx...],[xx,xx..]]
                    for row in data_tmp:
                        writer.writerow(row)
                else:
                    writer.writerow(data_tmp)

                writer.writerow("")

        elif type(data) == type([]) or type(data) == type(()):
            """
            data = [[xx,xx....], [xx,xx....], [xx,xx....].....]
            title => list
            """
            print 'csv_report.py => ', type(data)

            writer.writerow(title)
            for row in data:
                writer.writerow(row)
            writer.writerow("")

        csvfile.close()
        
        
if __name__ == '__main__':
    csv_report = csv_report()
    data = {u'标题':['2','d','f']}
    file_name = 'sadaasdas'
    d = csv_report.do_report(data, file_name)
