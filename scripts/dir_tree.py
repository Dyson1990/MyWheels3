﻿# -*- coding:utf-8 -*-  
"""
@Version: ??
@Author: Dyson
@Contact: Weaver1990@163.com
@File: file_tree.py
@Time: 2016/9/22 15:00
@Instruction：I will finish the annotation later, thanks ontherd for his blog:http://blog.chinaunix.net/uid-21374062-id-5198995.html
Not finish with the gbk code yet !!!!
"""
import set_log #log_obj.debug(文本)  "\x1B[1;32;41m (文本)\x1B[0m"
import os
import re

file_dir = {}
times = 0

def dirs_tree(startPath):
    startPath = os.path.normpath(startPath)
    # f = open('Folder(%s)_Tree.txt' %os.path.split(startPath)[1], 'w')
    f = open('Folder_Tree.txt', 'w')
    '''树形打印出目录结构'''
    for root, dirs, files in os.walk(startPath):
        print("Checking %s" %root)
        #获取当前目录相对输入目录的层级关系,整数类型
        level = root.replace(startPath, '').count(os.sep)
        #树形结构显示关键语句
        #根据目录的层级关系，重复显示'| '间隔符，
        #第一层 '| '
        #第二层 '| | '
        #第三层 '| | | '
        #依此类推...
        #在每一层结束时，合并输出 '|____'
        indent_dir = '|*' * 1 * level + '|--'
        # if files:
        #     content = '%s%s ---files included:%s \n' % (indent, os.path.split(
        #                         root)[1], files)
        #     print "Type(content1):%s" % type(content)
        #     f.write(content)
        # else:
        #     content = '%s%s \n' % (indent, os.path.split(root)[1])
        #     print "Type(content2):%s" %type(content)
        #     f.write(content)
        dir_content = '%s%s\\\n' % (indent_dir, os.path.split(root)[1])
        f.write(dir_content)
        if files:
            for file in files:
                indent_file = ' ' * (len(os.path.split(root)[1])+ len(indent_dir)) + '|_'
                content = '%s%s\n' % (indent_file,file)
                f.write(content)
    f.close()

def dirs_tree_filtered(startPath):
    startPath = os.path.normpath(startPath)
    tree = ''
    tree_ignore = []
    for root, dirs, files in os.walk(startPath):
        if root in tree_ignore:
            for dir0 in dirs:
                tree_ignore.append(os.path.join(root, dir0))
            continue
        for dir0 in dirs:
            if re.search(r'\.|__', dir0):
                tree_ignore.append(os.path.join(root, dir0))
        level = root.replace(startPath, '').count(os.sep)
        indent_dir = '|*' * 1 * level + '|--'
        dir_content = '%s%s\\\n' % (indent_dir, os.path.split(root)[1])
        tree = tree + dir_content
        if files:
            for file in files:
                indent_file = ' ' * (len(os.path.split(root)[1])+ len(indent_dir)) + '|_'
                content = '%s%s\n' % (indent_file,file)
                tree = tree + content
    
    return tree	
	
if __name__ == '__main__':
    # dir = raw_input('please input the path:')
    # dir = r'E:\Download\新建文件夹'
    dir0 = r'C:\Users\gooddata\PycharmProjects\pipelining_init\pipelining'
    # list_files(dir)
    print(dirs_tree_filtered(dir0))
