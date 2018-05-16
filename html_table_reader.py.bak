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
import re

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')

class html_table_reader(object):
    def __init__(self):
        pass

    def table_tr_td(self, e_table, fill_method = None, start_row = 0):
        """
        主要是为了针对有合并单元格的网页table写的，将含有合并单元格的表格放进Dataframe的结果还有待考虑

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
        for r in xrange(row_count):
            row = e_trs[r]
            e_tds = row.find_all('td')
            i = 0 # 为了跳过已经填好None值的单元格，直接用列序号会报错
            has_colspan = False
            for c in xrange(col_count):
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
                    for j in xrange(1, min(col_count-c,int(e_td['colspan']))):
                        df.iloc[r, c + j] = None
                # 竖向合并的单元格
                if e_td.has_attr('rowspan'):
                    # 有些'rowspan'会超出表格高度
                    for j in xrange(1, min(row_count-r,int(e_td['rowspan']))):
                        df.iloc[r + j, c] = None
                df.iloc[r, c] = e_td.get_text(strip=True)
                i = i + 1
            if has_colspan and fill_method:
                df.iloc[r,:] = df.iloc[r,:].fillna(method = fill_method)
        # 防止在读写json的时候出现顺序问题
        #df.index = [str(i) for i in df.index]
        #df.columns = [str(i) for i in df.columns]
        if df.empty:
            df = pd.read_html(e_table.prettify(), encoding='utf8')
        return df

    def title_standardize(self, df, delimiter='=>', b0 = True, fillna_method='ffill'):
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

        df.index = range(len(df.index)) # 索引重新从0计算
        return df

    def data_standardize(self, df, delimiter=r'/\n/'):
        for r in xrange(df.shape[0]-1, 0, -1):
            if df.iloc[r,:].hasnans:
                df.iloc[r-1, :] = df.iloc[r-1, :] + (delimiter + df.iloc[r, :]).fillna('')
                df = df.drop(r,axis=0)
        df.index = range(len(df.index))  # 索引重新从0计算
        return df

    def standardize(self, df, delimiter=r'/\n/', b0 = True):
        df = self.title_standardize(df, delimiter, b0)
        df = self.data_standardize(df, delimiter)

        return df



if __name__ == '__main__':
    s = """
<table cellpadding="0" cellspacing="0" border="0">
					<tbody><tr style="color:#ffffff;">
						<td width="35px" class="xz_line" height="24px" bgcolor="#8BB3D7" align="center">序号</td><td width="805px" class="xz_line" bgcolor="#8BB3D7" align="center">文件名</td><td width="48px" bgcolor="#8BB3D7" align="center">下载</td>
					</tr>
					
					 
						<tr>
							<td class="xz_line" height="24px" bgcolor="#FAFAFA" align="center">1</td><td class="xz_line" bgcolor="#FAFAFA" align="left">10号工业挂牌出让文件.doc</td><td bgcolor="#FAFAFA" align="center">
							<a href="#" onclick="isLogin('1333','10号工业挂牌出让文件.doc');" cssclass="xz_pic">
								<img src="images/list_09.jpg" title="点击下载" alt="点击下载">
							</a></td>
						<!-- 	
								
								
							
							<a href=" download?RECORDID=1333&amp;fileName=10%BA%C5%B9%A4%D2%B5%B9%D2%C5%C6%B3%F6%C8%C3%CE%C4%BC%FE.doc" class="xz_pic"><img src="images/list_09.jpg" title="点击下载" alt="点击下载" /></a></td>
						 -->
						</tr>
					 
					
					 
						<tr>
							<td class="xz_line" height="24px" bgcolor="#FAFAFA" align="center">2</td><td class="xz_line" bgcolor="#FAFAFA" align="left">挂牌授权委托书和法定代表人证明书.doc</td><td bgcolor="#FAFAFA" align="center">
							<a href="#" onclick="isLogin('1244','挂牌授权委托书和法定代表人证明书.doc');" cssclass="xz_pic">
								<img src="images/list_09.jpg" title="点击下载" alt="点击下载">
							</a></td>
						<!-- 	
								
								
							
							<a href=" download?RECORDID=1244&amp;fileName=%B9%D2%C5%C6%CA%DA%C8%A8%CE%AF%CD%D0%CA%E9%BA%CD%B7%A8%B6%A8%B4%FA%B1%ED%C8%CB%D6%A4%C3%F7%CA%E9.doc" class="xz_pic"><img src="images/list_09.jpg" title="点击下载" alt="点击下载" /></a></td>
						 -->
						</tr>
					 
					
					 
						<tr>
							<td class="xz_line" height="24px" bgcolor="#FAFAFA" align="center">3</td><td class="xz_line" bgcolor="#FAFAFA" align="left">象山经济开发区城东工业园工业待出让C-2-07-01地块规划设计条件.pdf</td><td bgcolor="#FAFAFA" align="center">
							<a href="#" onclick="isLogin('1245','象山经济开发区城东工业园工业待出让C-2-07-01地块规划设计条件.pdf');" cssclass="xz_pic">
								<img src="images/list_09.jpg" title="点击下载" alt="点击下载">
							</a></td>
						<!-- 	
								
								
							
							<a href=" download?RECORDID=1245&amp;fileName=%CF%F3%C9%BD%BE%AD%BC%C3%BF%AA%B7%A2%C7%F8%B3%C7%B6%AB%B9%A4%D2%B5%D4%B0%B9%A4%D2%B5%B4%FD%B3%F6%C8%C3C-2-07-01%B5%D8%BF%E9%B9%E6%BB%AE%C9%E8%BC%C6%CC%F5%BC%FE.pdf" class="xz_pic"><img src="images/list_09.jpg" title="点击下载" alt="点击下载" /></a></td>
						 -->
						</tr>
					 
					
				</tbody></table>"""
    #html_table_reader = html_table_reader()
    #df = html_table_reader.table_tr_td(s,None)
    #df.to_csv('df.csv', encoding='utf_8_sig')
    #print df
    #print df.empty
    #print df.iloc[0,0].replace(u'\xa0','')
    #print html_table_reader.standardize(df)
    #print pd.read_html(s,encoding='utf8')

    bs_obj = bs4.BeautifulSoup(s,'html.parser')
    e_table = bs_obj.find('table')
    e_tr = e_table.find_all('tr')[-1]
    print e_tr
    #print e_tr.string
    #print e_tr.a.string