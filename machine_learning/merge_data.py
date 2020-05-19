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


def get_filepaths(path, extension):
    """返回一个文件夹下所有的对应扩展名的文件名"""
    all_files = os.listdir(path) # 全部文件名
    # 获取扩展名，筛选扩展名是不是所需要的
    #print [os.path.splitext(s)[1] for s in all_files]
    filenames = [s for s in all_files if os.path.splitext(s)[1] == extension]
    # 合并路径和文件名
    return [os.path.join(path, s) for s in filenames]

def merge_xls(filepaths, output_path, output_filename):
    df = pd.DataFrame([])
    for filename in filepaths:
        df = df.append(pd.read_excel(filename))
    df.index = list(range(df.shape[0]))
    df.to_excel(os.path.join(output_path,output_filename))

def merge_csv(filepaths, output_path, output_filename):
    df = pd.DataFrame([])
    for filename in filepaths:
        df = df.append(pd.read_csv(filename))
    df.index = list(range(df.shape[0]))
    df.to_csv(os.path.join(output_path,output_filename), encoding='utf_8_sig')

def rename_xls(filenames):
    path = os.path.split(filenames[0])[0]
    filenames = [os.path.split(filename)[1] for filename in filenames]
    print(filenames[0])
    print('path',path)
    max_len = min(max([len(filename) for filename in filenames]),8)
    rand_ints = random.sample(range(pow(10,max_len), pow(10,max_len+1)), len(filenames))
    for i in range(len(filenames)):
        filename = filenames[i]
        print(os.path.join(path, filename))
        if os.path.isfile(os.path.join(path, filename)) == True:
            newname = str(rand_ints[i]) + os.path.splitext(filename)[1]
            os.rename(os.path.join(path, filename), os.path.join(path, newname))


if __name__ == '__main__':
    path = r'D:\Users\lenovo\Desktop\Projects\PythonProgramming\crawler\data'
    filepaths = get_filepaths(path, '.csv')
    #merge_data.rename_xls(filenames)
    merge_csv(filepaths,path,'2017年综合评价录取名单.csv')
