# -*- coding:utf-8 -*-  

import bs4
import requests_manager

mod_dict = {
    "bs4":bs4,
    "requests_manager":requests_manager
}

class func_manager(object):
    def get_func(self, s):
        # 分解类似bs4.BeautifulSoup.get_text这样中间不需要参数的函数
        if s == 'self':
            return None

        func_list = s.split(".")
        func = mod_dict[func_list[0]]
        if len(func_list) == 1:
            return func
        else:
            for s in func_list[1:]:
                func = getattr(func, s)
        print type(getattr('self','run_func'))
        return func

    def run_entire_func(self, s, args):
        """
        分解类似bs4.BeautifulSoup(str, 'html.parser').find('td', attrs={"class":"normal"})这样中间需要参数的函数

        args = {
           "BeautifulSoup":{
               "l":["str", 'html.parser']
           } ,
           "find":{
               "l":['td'],
               "d":{
                   "attrs":{"class":"normal"}
               }
           }
        }
        """
        if s == 'self':
            return None

        func_list = s.split(".")
        func = mod_dict[func_list[0]]
        if len(func_list) == 1:
            return func
        else:
            for s in func_list[1:]:
                func = getattr(func, s)
                l = []
                d = {}
                if s in args:
                    if "l" in args[s]:
                        l = args[s]["l"]
                    if "d" in args[s]:
                        d = args[s]["d"]

                func = func(*l,**d)

        return func

    def run_partial_func(self, start_obj, s, args):
        """
        分解类似bs4.BeautifulSoup(str, 'html.parser').find('td', attrs={"class":"normal"})这样中间需要参数的函数

        args = {
           "BeautifulSoup":{
               "l":["str", 'html.parser']
           } ,
           "find":{
               "l":['td'],
               "d":{
                   "attrs":{"class":"normal"}
               }
           }
        }
        """
        if s == 'self':
            return None

        func_list = s.split(".")
        obj = start_obj
        for s in func_list:
            func = getattr(obj, s)
            l = []
            d = {}
            if s in args:
                if "l" in args[s]:
                    l = args[s]["l"]
                if "d" in args[s]:
                    d = args[s]["d"]

            print "runing func:%s,\nargs:'l':%s,'d':%s" % (s, l, d)
            obj = func(*l,**d)
        print "return obj, type:", type(obj)
        return obj

if __name__ == "__main__":
    func_manager = func_manager()
    s = """'<p>\n\t<span style="font-size:14px;"><strong>\xe6\x95\x99\xe6\x8e\x88\xe5\xb2\x97</strong></span><span style="font-size:14px;">\xef\xbc\x9a</span> \n</p>'"""
    #bs4.BeautifulSoup(s,'html.parser').find('td', "attrs": {"class": "normal"})
    args = {
        "BeautifulSoup": {
            "l": [s, 'html.parser']
        },
        "find": {
            "l": ['span'],
            "d": {
                "attrs": {"style": "font-size:14px;"}
            }
        }
    }
    #print func_manager.run_func("bs4.BeautifulSoup.find", args)
    print func_manager.get_func("bs4.BeautifulSoup.get_text")


