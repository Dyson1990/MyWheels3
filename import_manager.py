# -*- coding: utf-8 -*-
"""
Created on Fri May 17 16:25:09 2019

@author: gooddata
"""
import inspect
import pkgutil

def get_obj(dir_path, mod_name, obj_name=None):
    """
    返回pipelining这个项目下的一个对象
    dir_path: str
    mod_name: str
    """
    importer = pkgutil.get_importer(dir_path) # 返回一个FileFinder对象
    loader = importer.find_module(mod_name) # 返回一个SourceFileLoader对象
    mod = loader.load_module() # 返回需要的模块
    if obj_name:
        obj = getattr(mod, obj_name)
        return obj
    else:
        return mod

def get_class(dir_path, mod_name, class_name):
    """
    dir_path：包含需要的类的模块的目录名,str
    mod_name: 包含需要的类的模块名,str
    class_name：类名,str
    """
    class_obj = get_obj(dir_path, mod_name, class_name)
    if inspect.isclass(class_obj):
        return class_obj
    else:
        raise(TypeError('{}目录下，{}中的{}不是一个class').format(dir_path
                                                                  , mod_name
                                                                  , class_name)
                    )

def get_func(dir_path, mod_name, func_name, class_name=None):
    """
    dir_path：包含需要的类的模块的目录名,str
    mod_name: 包含需要的类的模块名,str
    func_name：函数名,str
    class_name：类名,str
    """
    if class_name:
        class_obj = get_obj(dir_path, mod_name, class_name)
        func_obj = getattr(class_obj, func_name)
    else:
        func_obj = get_obj(dir_path, mod_name, func_name)
    
    if inspect.isfunction(func_obj):
        return func_obj
    else:
        raise(TypeError('{}目录下，{}中没有名为{}的function').format(dir_path
                                                                    , mod_name
                                                                    , func_name)
                    )
    
def test(arg1,arg2=None,*arg, **kwarg):
    print('arg1', arg1)
    print('arg2', arg2)
    print('arg', arg)
    print('kwarg', kwarg)
    return None

if __name__ == '__main__':
    test(**{'arg1':'123423', 'arg2':'dsfasd', 'wtf':'asdf', '123':'123'})
    print(get_class('./', 'google_api', 'google_api'))