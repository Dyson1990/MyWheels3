# -*- coding:utf-8 -*-  
"""
@Version: ??
@Author: Dyson
@Contact: Weaver1990@163.com
"""
import os
import codecs

def files2md(dir_path, save_path, file_type):
    # 由于os.walk返回的是一个三元素的元祖，我们可以直接在for循环中对他们进行一一对应，简化代码。
    s_sum = ''
    for path, dir_list, file_list in os.walk(dir_path):
        for file_name in file_list: # 这里其实可以用列表生成式简化
            if os.path.splitext(file_name)[-1] in file_type:  #'.js', '.css' ('.py', '.json', '.html')
                file_path = os.path.join(path, file_name) # 生成文件路径
                print(file_path)
                # 读取文件
                with codecs.open(file_path, 'r', 'utf-8') as f:
                    s = f.read()
                # 按Markdown语法整理字符串
                title = '# {}'.format(file_name) # Markdown中的一级标题的语法
                code = "```\n{}\n```".format(s) # Markdown中的代码语法
                # 拼接到与之前的内容上
                s_sum = "{}\n{}\n{}".format(s_sum, title, code) 
                
    with codecs.open(save_path, 'w', 'utf-8') as f:
        f.write(s_sum) 
	
if __name__ == '__main__':
    dir0 = r'C:\Users\gooddata\Desktop\作业文件'
