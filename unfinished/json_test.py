# -*- coding: utf-8 -*-
"""
Created on Wed Jul 3 17:35:23 2019

@author: gooddata
"""
import itertools

class json_class:
    def __init__(self, data, level, parent):
        print(data)
        self.level = level
        self.parent = parent
        if level == 0 and isinstance(data, list):
            data = {i: item for i, item in enumerate(data)}
        gen = itertools.groupby(data
                                , key=lambda k:isinstance(data[k], (dict,list)))
        for bool0, gen0 in gen:
            if bool0:
                self.remain = {k: data[k] for k in gen0}
            else:
                self.data = tuple(gen0)
     
def separate_json_v5(json_obj, res=[]): 
    if not isinstance(json_obj, json_class):
        json_obj = json_class(json_obj, 0, None)
    if hasattr(json_obj, 'remain'):
        level0 = json_obj.level
        for k,v in json_obj.remain.items():
            if isinstance(v, list):
                for v0 in v:
                    obj0 = json_class({k:v0}, level=level0+1, parent=k)
                    res = separate_json_v5(obj0, res=res)
            else:
                obj0 = json_class(v, level=level0+1, parent=k)
                res = separate_json_v5(obj0, res=res)
    res.append(json_obj)
    return res


# 记录每次分解之间的联系，缺点是每一级的key都不可重复
def separate_json_v4(json_data, key=None, res=[], mapping_list={}): 
    if isinstance(json_data, list):
        json_data = {i: item for i, item in enumerate(json_data)}
    if isinstance(json_data, dict):
        for k,v in json_data.items():
            if key is not None:
                if key not in mapping_list:
                    mapping_list[key] = {k}
                else:
                    mapping_list[key].add(k)
            if isinstance(v, list):
                for i,v0 in enumerate(v):
                    res, mapping_list = separate_json_v4(v0
                                                         , res=res
                                                         , key=k
                                                         , mapping_list=mapping_list)
            else:
                res, mapping_list = separate_json_v4(v
                                                     , res=res
                                                     , key=k
                                                     , mapping_list=mapping_list)
    else:
        res.append({key:json_data})
    return res, mapping_list

# 代码功能重复
def separate_json_v3(json_data, key=None, res=[]): 
    if isinstance(json_data, list):
        json_data = {i: item for i, item in enumerate(json_data)}
    if isinstance(json_data, dict):
#        target = {k: v for k, v in json_data.items() if not isinstance(v, (dict,list))}
#        if target:
#            res.append({key:target})
#        remain = filter(lambda tup:isinstance(tup[1], (dict,list)), json_data.items())
        for k,v in json_data.items():
            if isinstance(v, list):
                for i,v0 in enumerate(v):
                    res = separate_json_v3(v0, res=res, key=k)
            else:
                res = separate_json_v3(v, res=res, key=k)
    else:
        res.append({key:json_data})
    return res

# 更新，将列表转化字典的key换成列表上一级字典的key
def separate_json_v2(json_data, key=None, res=[]): 
    # 由于之后每次使用separate_json_v2函数，传入的对象都是字典，所以此处只是针对最外层是列表的情况
    if isinstance(json_data, list):
        json_data = {i: item for i, item in enumerate(json_data)}
    if isinstance(json_data, dict):
        target = {k: v for k, v in json_data.items() if not isinstance(v, (dict,list))}
        if target:
            res.append({key:target})
        remain = filter(lambda tup:isinstance(tup[1], (dict,list)), json_data.items())
        for k,v in remain:
            # 如果是列表，那么就把其对应的key都换成上一级的字典的key
            if isinstance(v, list):
                for i,v0 in enumerate(v):
                    res = separate_json_v2(v0, res=res, key=k)
            else:
                res = separate_json_v2(v, res=res, key=k)
    else:
        # 存入非list或者dict的部分
        res.append({key:json_data})
    return res

# 最普通的分解，列表转化为其索引对应的字典
def separate_json_v1(json_data, key=None, res=[]):
    """
    这里的json_data必须是字典，因为第一行代码就用了items()方法
    """
    # 首先，对每个传入的json对象进行筛选
    target = {k: v for k, v in json_data.items() if not isinstance(v, (dict,list))}
    # 存入无法继续分解的数据
    if target:
        res.append(target)
    # 筛选出还能继续分解的元素
    remain = filter(lambda tup:isinstance(tup[1], (dict,list)), json_data.items())
    for k,v in remain:
        if isinstance(v, list):
            v = {i: v0 for i,v0 in enumerate(v)}
        res = separate_json_v1(v, res=res, key=k) # 再次使用原函数处理字段对象
    return res

if __name__ == '__main__':
    d = {
    	"col_a": {
    		"index1": [{"detail1": ["qy11", "qy12"]}, {"detail2": "qy3"}, {"YEAR": 1996}],
    		"index2": [{"detail1": ["qy21", "qy22"]}, {"detail2": "qy4"}, {"YEAR": 1987}]
    	},
    	"col_b": {
    		"index1": {'row1': 'qy11'},
    		"index2": {'row2': 'qy51'}
    	},
    	"col_c": {
    		"index1": "321",
    		"index2": "123"
    	},
    	"key": {
    		"index1": "row1",
    		"index2": "row2"
    	}
    }
    
#    json_obj = json_class(d, 0, None)
#    print(json_obj.remain)
    print(separate_json_v1(d))
    print(separate_json_v2(d))
    print(separate_json_v3(d))
    print(separate_json_v4(d))
    print([obj.data for obj in separate_json_v5(d)])
