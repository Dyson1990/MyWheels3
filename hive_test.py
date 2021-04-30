# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 20:36:46 2020

@author: Administrator
"""

from pyhive import hive   # or import hive
conn = hive.Connection(host='192.168.0.116'
                       , port=10000
                       # , username='Dyson'
                        # , password=122321
                       , database='default'
                        , auth='NONE'
                       )
cur = conn.cursor()
# cur = hive.Connection(host='192.168.0.116', port=10000).cursor()
resp = cur.execute('SELECT * FROM Alice LIMIT 10')

print(resp.fetchall())