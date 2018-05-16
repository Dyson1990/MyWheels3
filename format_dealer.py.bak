# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: format_dealer.py
    @time: 2017/3/15 14:23
    @info: 个人常用代码
--------------------------------
"""

import datetime
import wx
import sys

class format_dealer():
    
    def __init__(self):
        pass
        
    def wxdate2date(self, datetime_dic, end_date_list = [], start_date_list = []):
        """
        
        """
        for key in datetime_dic:
            if type(datetime_dic[key]) == type(wx.DateTime_Today()):
                datetime_dic[key] = datetime.datetime(datetime_dic[key].Year, datetime_dic[key].Month+1,
                                                      datetime_dic[key].Day,datetime_dic[key].Hour,
                                                      datetime_dic[key].Minute,datetime_dic[key].Second)
        # 增加小时，分钟，秒
        for s in end_date_list:
            datetime_dic[s] = datetime_dic[s] + datetime.timedelta(hours=23, minutes=59)

        
        # 检测时间输入
        if len(end_date_list) == len(start_date_list):
            check_list = [datetime_dic[end_date_list[i]] > datetime_dic[start_date_list[i]] for i in xrange(len(end_date_list))]
        
            if False in check_list:
                print u"""
                       datetime_dic: %s


                       输入时间有误！

                       """ % datetime_dic
                sys.exit()

        return datetime_dic