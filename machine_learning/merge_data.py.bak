# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: merge__data.py
    @time: 2017/9/7 14:50
--------------------------------
"""
import random
import sys
import os
import pandas as pd

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

class merge_data(object):
    def __init__(self):
        pass

    def get_filepaths(self, path, extension):
        """返回一个文件夹下所有的对应扩展名的文件名"""
        all_files = os.listdir(path) # 全部文件名
        # 获取扩展名，筛选扩展名是不是所需要的
        #print [os.path.splitext(s)[1] for s in all_files]
        filenames = filter(lambda s:os.path.splitext(s)[1] == extension, all_files)
        # 合并路径和文件名
        return [os.path.join(path, s) for s in filenames]

    def merge_xls(self, filepaths, output_path, output_filename):
        df = pd.DataFrame([])
        for filename in filepaths:
            df = df.append(pd.read_excel(filename))
        df.index = range(df.shape[0])
        df.to_excel(os.path.join(output_path,output_filename))

    def merge_csv(self, filepaths, output_path, output_filename):
        df = pd.DataFrame([])
        for filename in filepaths:
            df = df.append(pd.read_csv(filename))
        df.index = range(df.shape[0])
        df.to_csv(os.path.join(output_path,output_filename), encoding='utf_8_sig')

    def rename_xls(self, filenames):
        path = os.path.split(filenames[0])[0]
        filenames = [os.path.split(filename)[1] for filename in filenames]
        print filenames[0]
        print 'path',path
        max_len = min(max([len(filename) for filename in filenames]),8)
        rand_ints = random.sample(xrange(pow(10,max_len), pow(10,max_len+1)), len(filenames))
        for i in xrange(len(filenames)):
            filename = filenames[i]
            print os.path.join(path, filename)
            if os.path.isfile(os.path.join(path, filename)) == True:
                newname = str(rand_ints[i]) + os.path.splitext(filename)[1]
                os.rename(os.path.join(path, filename), os.path.join(path, newname))


if __name__ == '__main__':
    merge_data = merge_data()
    path = r'D:\Users\lenovo\Desktop\Projects\PythonProgramming\crawler\data'
    filepaths = merge_data.get_filepaths(path, '.csv')
    #merge_data.rename_xls(filenames)
    merge_data.merge_csv(filepaths,path,u'2017年综合评价录取名单.csv')
