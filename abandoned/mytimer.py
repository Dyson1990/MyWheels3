# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: timer.py
    @time: 2017/7/20 11:01
--------------------------------
"""
import time
import os
import sched
import sys
import datetime

"""

schedule库已经能更加灵活的制作定时任务了，所以此文件弃用


"""


# 初始化sched模块的scheduler类
# 第一个参数是一个可以返回时间戳的函数，第二个参数可以在定时未到达之前阻塞。
schedule = sched.scheduler(time.time, time.sleep)

start_time = 0
end_time = 0
        
# 被周期性调度触发的函数
def execute_command(cmd, inc):
    start_time = datetime.datetime.now()
    os.system(cmd)
    time.sleep(3)
    end_time = datetime.datetime.now()
    delay = round((end_time-start_time).total_seconds())
    print() 
    print('mytimer => 开始时间：%s' % start_time)
    print('mytimer => 耗时:%smin' %(delay/60))
    schedule.enter(int(inc-delay), 0, execute_command, (cmd, inc))
    print('mytimer => 结束时间：%s' % end_time)

def cmd_timer(cmd, time_str, inc=60):
    # enter四个参数分别为：间隔时间、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，
    # 给该触发函数的参数（tuple形式）
    now = datetime.datetime.now()
    schedule_time = datetime.datetime.strptime(time_str,'%H:%M').replace(year=now.year,month=now.month,day=now.day)
    if schedule_time < now:
        schedule_time = schedule_time + datetime.timedelta(days=1)
    time_before_start = int(round((schedule_time-datetime.datetime.now()).total_seconds()))
    print('mytimer => 还有%s秒开始任务' %time_before_start)
    schedule.enter(time_before_start, 0, execute_command, (cmd, inc))
    schedule.run()

if __name__ == '__main__':
    cmd_timer("netstat -an", '15:07', 60)
