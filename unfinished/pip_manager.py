# -*- coding: utf-8 -*-
"""
Created on Mon May 20 18:57:45 2019

@author: gooddata
"""

import pip
# pip V10.0.0以上版本需要导入下面的包
from pip._internal.utils.misc import get_installed_distributions
import subprocess
import time

print('pip版本为', pip.__version__)

def upgrade_all():
    #for dist in get_installed_distributions():
    #    print(dist.project_name)
    
    for dist in get_installed_distributions():
        print("updating:", dist.project_name, "\t")
        print(time.asctime( time.localtime(time.time()) ))
        # 执行后，pip默认为Python3版本
        # 双版本下需要更新Python2版本的包，使用py2运行，并将pip修改成pip2
        cmd = "pip install --user --upgrade " + dist.project_name
        print('准备执行', cmd)
        subprocess.call(cmd, shell=True)