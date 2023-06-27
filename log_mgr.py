# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 17:29:04 2022

@author: Weave
"""

from loguru import logger
from pathlib import Path

import os
import codecs
import datetime

py_dir = Path(__file__).parent
log_dir = py_dir.joinpath('log')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logger.add(log_dir.joinpath('driver.log'), filter=lambda d0: d0['function']=='driver_info', retention='1 day')

def w_log(fn, *contents, fd=log_dir):
    fp = log_dir.joinpath(fn)
    with codecs.open(fp, 'a', 'utf-8') as fw:
        fw.write(str(datetime.datetime.now())+'\n')
        
        for content0 in contents:
            fw.write(content0+'\n')
        fw.write('\n')
        
def driver_info(*msgs):
    logger.info(' '.join([str(obj) for obj in msgs]))
    
def print_exc(err):
    logger.exception(err)

    
if __name__ == '__main__':
    driver_info('3345')