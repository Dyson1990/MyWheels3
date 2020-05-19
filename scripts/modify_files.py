# -*- coding:utf-8 -*-  
"""
@Version: ??
@Author: Dyson
@Contact: Weaver1990@163.com
"""
import os
import codecs
        
def dir_files(dir_path, search_str, rep_str, file_type):
    # 由于os.walk返回的是一个三元素的元祖，我们可以直接在for循环中对他们进行一一对应，简化代码。
    for path, dir_list, file_list in os.walk(dir_path):
        for file_name in file_list: # 这里其实可以用列表生成式简化
            if os.path.splitext(file_name)[-1] in file_type:  #'.py', '.json', '.html'
                file_path = os.path.join(path, file_name) # 生成文件路径
                print(file_path)
                # 读取文件
                with codecs.open(file_path, 'r') as f:
                    s = f.read()
                s = s.replace(search_str, rep_str)
                with codecs.open(file_path, 'w') as f:
                    f.write(s) 

if __name__ == '__main__':
    dir0 = r'C:\Users\gooddata\Desktop\作业文件'
