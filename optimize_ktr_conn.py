#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May  8 14:15:32 2021

@author: wolf
"""

import lxml.etree as etree
import codecs

file_path = '/home/wolf/Documents/tmp_copy.ktr'

with codecs.open(file_path, 'r', 'utf-8') as fp:
    xml_l = fp.readlines()
    
tree = etree.XML('\n'.join(xml_l[1:]))


    
# =============================================================================
# ele_str = """
# <attribute><code>EXTRA_OPTION_MYSQL.rewriteBatchedStatements</code><attribute>true</attribute></attribute>
# """
# root_e = etree.Element('attribute')
# code_e = etree.Element('code')
# code_e.text = 'EXTRA_OPTION_MYSQL.rewriteBatchedStatements'
# attr_e = etree.Element('attribute')
# attr_e.text = 'true'
# root_e.append(code_e)
# root_e.append(attr_e)
# =============================================================================

conn_args = {
        'EXTRA_OPTION_MYSQL.rewriteBatchedStatements': 'true'
        , 'EXTRA_OPTION_MYSQL.useServerPrepStmts': 'false'
        , 'EXTRA_OPTION_MYSQL.defaultFetchSize': '500'
        , 'EXTRA_OPTION_MYSQL.useCompression': 'true'
        }
for conn_arg_e in tree.xpath('/transformation/connection/attributes'):
    for k0, v0 in conn_args.items():
        root_e = etree.Element('attribute')
        code_e = etree.Element('code')
        code_e.text = k0
        attr_e = etree.Element('attribute')
        attr_e.text = v0
        root_e.append(code_e)
        root_e.append(attr_e)
        
        conn_arg_e.append(root_e)

output_path = 'test.ktr'
etree.ElementTree(tree).write(output_path, pretty_print=True)

with open(output_path, 'r+', encoding='utf-8') as f:
    content = f.read()
    f.seek(0, 0)
    f.write(xml_l[0] + '\n' + content)