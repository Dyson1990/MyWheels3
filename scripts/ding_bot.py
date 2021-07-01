#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 14:09:47 2021

@author: wolf
"""

import dingtalkchatbot.chatbot as cb
import datetime
import sys
import platform

Today = datetime.datetime.now().strftime('%Y%m%d')
Hour = datetime.datetime.now().strftime('%Y%m%d%H')

os = platform.system()
if os == 'Windows':
    path_day = "C:\\Users\\hehe\\Desktop\\临时\\" +  Today + ".txt"
    path_hour = "C:\\Users\\hehe\\Desktop\\临时\\" +  Hour + ".txt"
else:
    path_day = "/home/edsuser/dingding_monitor/" +  Today + ".txt"
    path_hour = "/home/edsuser/dingding_monitor/" +  Hour + ".txt"


class dingRobot():

    def __init__(self):
        self.url = "https://oapi.dingtalk.com/robot/send?access_token=46c2497e888a4c4ef355272de02911987c33724545ea7026071a8919d3c26b76"

    def getMessage(self, filepath):
        message = ""
        for line in open(self.path, encoding="utf-8", errors="ignore"):
            message = message + line
        return message

    def dingStart(self):
        msg = self.getMessage()
        xiaoding = cb.DingtalkChatbot(self.url)
        xiaoding.send_text(msg=msg)
        
    def ding_report(self, msg, ding_mobile):
        xiaoding = cb.DingtalkChatbot(self.url)
        xiaoding.send_text(msg='parse_addr:\n' + msg
                           # , at_dingtalk_ids=['刘颖波']
                           , at_mobiles=[ding_mobile]
                           )
        
        
if __name__ == "__main__":
    obj_ding = dingRobot()
    obj_ding.ding_report('??????', '15168332383')
    
    # if sys.argv[1] == 'run1':
    #     dingding = dingRobot(path_day)
    #     dingding.dingStart()

    # elif sys.argv[1] == 'run2':
    #     dingding = dingRobot(path_hour)
    #     dingding.dingStart()
    # else:
    #     print("The argument was wrong! please use 'run1' or 'run2'")
    