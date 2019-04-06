# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: html_table_reader.py
    @time: 2017/7/19 16:35
    @instruction: table_tr_td => 解析html中tabel>tr>td这种格式的表格
                  standardize => 将解析过存储在df中的表格按需求做DIY
--------------------------------
"""
import sys
import bs4
import pandas as pd
import numpy as np



def table_tr_td(e_table, fill_method = None, start_row = 0):
    """
    主要是为了针对有合并单元格的网页table写的，将含有合并单元格的表格放进Dataframe的结果还有待考虑
    现在暂时不合并单元格

    :param e_table: bs4的table元素
    :param fill_method : 参数与fillna()中的method相同，选择填充方式，否则用None
    :return:
    """
    if not (isinstance(e_table, bs4.element.Tag) or isinstance(e_table, bs4.BeautifulSoup)):
        e_table = bs4.BeautifulSoup(e_table, 'html.parser')

    # 搭建表格框架
    df0 = pd.DataFrame(e_table.find_all('tr')[start_row:])
    df0[1] = df0[0].apply(lambda e:len(e.find_all('td')))
    col_count = max(df0[1])
    row_count = len(df0.index)
    df = pd.DataFrame(np.zeros([row_count, col_count]), dtype=int)

    # 根据网页中的表格，还原在dataframe中，有合并单元格现象的
    # 值填在第一个单元格中，其他的用None填充
    e_trs = df0[0].tolist()
    for r in range(row_count):
        row = e_trs[r]
        e_tds = row.find_all('td')
        i = 0 # 为了跳过已经填好None值的单元格，直接用列序号会报错
        has_colspan = False
        for c in range(col_count):
            if pd.isnull(df.iloc[r,c]):
                continue
            if i > len(e_tds)-1 and df.iloc[r,c]==0:
                df.iloc[r, c] = None
                continue
            e_td = e_tds[i]
            # 横向合并的单元格
            if e_td.has_attr('colspan'):
                has_colspan = True
                # 有些'colspan'会超出表格宽度
                for j in range(1, min(col_count-c,int(e_td['colspan']))):
                    df.iloc[r, c + j] = None
            # 竖向合并的单元格
            if e_td.has_attr('rowspan'):
                # 有些'rowspan'会超出表格高度
                for j in range(1, min(row_count-r,int(e_td['rowspan']))):
                    df.iloc[r + j, c] = None
            df.iloc[r, c] = e_td.get_text(strip=True)
            i = i + 1
        if has_colspan and fill_method:
            df.iloc[r,:] = df.iloc[r,:].fillna(method = fill_method)
    # 防止在读写json的时候出现顺序问题
    # df.index = [str(i) for i in df.index]
    # df.columns = [str(i) for i in df.columns]
    if df.empty:
        df = pd.read_html(e_table.prettify(), encoding='utf8')
    return df

def title_standardize(df, delimiter='=>', b0 = True, fillna_method='ffill'):
    """将数据的标题与数据分离，将有合并单元的行合并"""
    if b0 and df.iloc[0,:].hasnans and df.iloc[1,:].hasnans:# 假设第一排数据行没有横向合并单元格
        if fillna_method:
            df.iloc[0, :] = df.iloc[0, :].fillna(method=fillna_method) + (delimiter + df.iloc[1,:]).fillna('')
        else:
            df.iloc[0, :] = df.iloc[0, :].fillna('') + (delimiter + df.iloc[1,:]).fillna('')
        df = df.drop([1,], axis=0)

    df.columns = df.iloc[0,:]
    df.columns.name = None
    df = df.drop([0,], axis=0)

    df.index = list(range(len(df.index))) # 索引重新从0计算
    return df

def data_standardize(df, delimiter=r'/\n/'):
    # 若数据行r存在空白单元格，则与r-1行的数据合并
    for r in range(df.shape[0]-1, 0, -1):
        if df.iloc[r,:].hasnans:
            df.iloc[r-1, :] = df.iloc[r-1, :] + (delimiter + df.iloc[r, :]).fillna('')
            df = df.drop(r,axis=0)
    df.index = list(range(len(df.index)))  # 索引重新从0计算
    return df

def standardize(df, delimiter=r'/\n/', b0 = True):
    # 将标题行和数据行全部标准化
    df = title_standardize(df, delimiter, b0)
    df = data_standardize(df, delimiter)

        return df



if __name__ == '__main__':
    html_table_reader = html_table_reader()
