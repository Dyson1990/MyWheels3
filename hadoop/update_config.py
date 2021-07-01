#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 20:30:27 2020

@author: wolf
"""
import xml
import xml.etree.ElementTree as et
import codecs
import regex
# import lxml.etree

hadoop_dir = '/usr/share/hadoop3/'

# def update_by_xpath(config_path, xpath):
#     et.register_namespace("text/xsl", "configuration.xsl")
#     et_root = et.parse(config_path)
#     
#     print(dir(xml.etree))
#     for doc in et_root.getroot():
#         print(dir(doc))
#         print(doc.tag)
#         doc.find('name').text = '123'
#         print(doc.find('name').text)
#         break
#     
#     et_root.write(config_path, encoding='utf-8', xml_declaration=True)

def update_by_re(config_path, conf_d = {'datanucleus.schema.validateConstraints': None}):
    with codecs.open(config_path, 'r', 'utf-8') as fp:
        xml = fp.read()
        
    for k0,v0 in conf_d.items():
        re_str = "<name>(?P<key>{})</name>\s+<value>(?P<value>\w+)</value>".format(k0)
        m1 = regex.search(re_str, xml, regex.M)
        re_str = "<name>(?P<key>{})</name>\s+<value />".format(k0)
        m2 = regex.search(re_str, xml, regex.M)
        re_str = "<name>(?P<key>{})</name>\s+(?P<value><value.+?>)".format(k0)
        m3 = regex.search(re_str, xml, regex.M)
        if m1 and v0:
            target_dict = m1.groupdict()
            target_str = m1.group()
            target_str_new = target_str.replace(target_dict['value'], v0)
            xml = xml.replace(target_str, target_str_new)
            
        elif m2 and v0:
            target_str = m2.group()
            target_str_new = target_str.replace('<value />', '<value>{}</value>'.format(v0))
            xml = xml.replace(target_str, target_str_new)
            
        elif m3 and v0 is None:
            target_dict = m3.groupdict()
            xml = xml.replace(target_dict['value'], '<value />')
            
            
    with codecs.open(config_path, 'w', 'utf-8') as fp:
        fp.write(xml)
        
def load_xml(config_path):
    with codecs.open(config_path, 'r', 'utf-8') as fp:
        xml = fp.read()
    
    re_str = "<name>(?P<key>.+)</name>\s+(<value>(?P<value>[^<>]+?)</value>|<value />)"
    config_dict = {tup0[0]: tup0[2] for tup0 in regex.findall(re_str, xml)}
    print(config_dict)
    
    # m = regex.search(re_str, xml, regex.M)
    # if m:
    #     while True:
    #         print(m.capturesdict())
    # print(config_list)
    
if __name__=='__main__':
    # update_by_re('hive-site.xml')
    load_xml('hive-site.xml')