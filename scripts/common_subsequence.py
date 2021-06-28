#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import difflib

re_dict = {
    "街路巷弄名": "西路|大道|大街|南路|北路|中路|东路|里|道|路|街|弄|巷" # |区
    , "自然村": "行政村|自然村|村"
    , "住宅小区": "[小一二三四五六七八九东西南北]区|花园|公寓|新村|家园|公馆|名苑|苑|庭|园|城|府" # |村
    , "商业广场": "广场|中心"
    , "写字楼": "大厦|商厦"
    }

def common_subsequence(str1, str2):
    diff = difflib.Differ()
    output = []
    tmp_l = []
    for i0, s0 in enumerate(diff.compare(str1, str2)):
        if s0.startswith(' '):
            tmp_l.append(s0[-1])
        
        elif tmp_l:
            output.append((''.join(tmp_l), i0))
            tmp_l = []
    return tuple(output)

if __name__ == '__main__':
    str1 = 'XX路123号ABC小区1幢'
    str2 = 'XX路ABC小区1幢1单元101室'
    print(common_subsequence(str1, str2))
