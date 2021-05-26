#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 11:07:08 2021

@author: wolf
"""

import sys
import codecs
import os

args = {
        'name': 'Kettle' # 必填
        , 'exec': os.path.abspath('~/Program/data-integration8.2/spoon.sh') # 必填
        , 'encoding': 'UTF-8'
        , 'icon': os.path.abspath('~/Program/data-integration8.2/spoon.ico')
        }

file_format = """
[Desktop Entry]
Encoding={encoding}
Name={name}
Comment=
Exec={exec}
Icon={icon}
Terminal=false
StartupNotify=true
Type=Application
Categories=Application;Development;
"""

output = file_format.strip().format(**args)
print(output)

file_dir = '/usr/share/applications'
file_path = os.path.join(file_dir, args['name']+'.desktop')
with codecs.open(file_path, 'w', 'utf-8') as fp:
    fp.writable(output)
    
os.system('sudo chmod u+x '+file_path)
    
    
    
    
    
    