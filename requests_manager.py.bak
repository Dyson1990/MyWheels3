# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: requests_manager.py
    @time: 2017/10/13 9:49
--------------------------------
"""
import sys
import os
import random
import requests
import urllib2, sys
import json

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')


user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class requests_manager(object):
    def __init__(self):

        self.user_agent = random.choice(user_agent_list)
        self.headers = {'Accept': '*/*',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Cache-Control': 'max-age=0',
                        'User-Agent': self.user_agent,
                        # 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                        'Connection': 'keep-alive'
                        }

    def get_html(self, url, **kwargs):

        headers = kwargs['headers'] if 'headers' in kwargs else self.headers

        cookies = kwargs['cookies'] if 'cookies' in kwargs else None

        self.headers['User-Agent'] = random.choice(user_agent_list)
        print "user_agent:", self.headers['User-Agent']

        resp = requests.get(url, headers=headers, cookies=cookies)
        resp.encoding = resp.apparent_encoding
        resp.raise_for_status()

        html = resp.text
        resp.close()
        return html

    def get_file(self, url, targetfile):
        r = requests.get(url, headers=self.headers)
        with open(targetfile, "wb") as code:
            code.write(r.content)
            print "====>>>Successfully saving %s" %targetfile

if __name__ == '__main__':
    requests_manager = requests_manager()
    # print requests_manager.get_html('http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=002450+PEG')
    # s = "fyr_ssid_n5776=fyr_n5776_jbx7scxb; guest_id=1501663389; rz_utm_source=8; LXB_REFER=www.baidu.com; regsms=1514854962000; stat_sessid=miq8epg3b9sj42csi5ifsdtk73; PHPSESSID=m5jvh5ec3gkk9ie1silpghqps4; had_quiz_55635%09user_13575486859%09VFJRD1BWBQ9eUFgHBFdUUFdVCwFQBwZUCVVSVlFXUgo%3D9b207ecd5c=1514855022000; cur_ck_time=1514856051; ck_request_key=k9tVO1%2FFyDR%2FLNBjIA0j8Q8tEfWnKtN9lgMYR%2FUKBjQ%3D; http_tK_cache=dd7f2bcd2533e1cbb6c096a2f8ac5b93674b43d4; passport=55635%09user_13575486859%09VFJRD1BWBQ9eUFgHBFdUUFdVCwFQBwZUCVVSVlFXUgo%3D9b207ecd5c; rz_u_p=d41d8cd98f00b204e9800998ecf8427e%3Duser_13575486859; rz_rem_u_p=aiFB3odpeWZHIeDOt%2FJ%2BaNkn%2F8V390t5nnkC3N3%2FbHM%3D%24KzJx4oUsxjHHhuNbZ9EmS5OMgDiO8JGftPoh1SVUL24%3D; smppw_tz_auth=1; Hm_lvt_c3f6328a1a952e922e996c667234cdae=1512976537,1512977850,1513046435,1514854963; Hm_lpvt_c3f6328a1a952e922e996c667234cdae=1514872806; rz_token_6658=b8d8dcb26d087fa6424d729f4781e8c1.1514872805; autologin_status=0"
    # cookies = dict([s0.split('=') for s0 in s.split('; ')])
    # print cookies
    #
    # headers = {
    #     'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    #     'Accept-Encoding':'gzip, deflate',
    #     'Accept-Language':'zh-CN,zh;q=0.9',
    #     'Cache-Control':'max-age=0',
    #     'Connection':'keep-alive',
    #     'Host':'dc.simuwang.com',
    #     'Referer':'http://dc.simuwang.com/product/HF00000STD.html',
    #     'Upgrade-Insecure-Requests':'1',
    #     'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'
    # }
    # # print headers
    # with open('test.html','w') as f:
    #     f.write(requests_manager.get_html('http://dc.simuwang.com/product/HF00000STD.html', cookies=cookies, headers=headers))

    # http://dc.simuwang.com/product/HF00000STD.html

    import pandas as pd
    import numpy as np
    import json
    import traceback
    import bs4
    import re
    import datetime
    import time
    #
    stock_list = pd.read_excel('C:\Users\Administrator\Desktop\stock_list.xlsx', dtype=np.str)
    stock_list = stock_list.set_index("stock_code")

    output = pd.DataFrame([])
    for i in range(stock_list.shape[0]):
        try:
            stock_code = stock_list.index[i]
            print 'stock:', stock_code

            resp = requests_manager.get_html('http://data.eastmoney.com/dxf/q/%s.html' %stock_code)
            bs_obj = bs4.BeautifulSoup(resp, 'html.parser')
            e_table = bs_obj.find('div', class_='contentBox').table
            df = pd.read_html(e_table.prettify(encoding='utf8'), encoding='utf8')[0]
            df.columns = [u'序号', u'解除限售日期', u'占总股本比例%', u'数量（万股）',u'最新价（元）',u'当前市值（亿元）',u'限售股东一览']
            df['date'] = pd.to_datetime(df[u'解除限售日期']).copy()
            print df
            df = df[df['date'].between(datetime.datetime.now(), datetime.datetime(year=2200, month=1, day=1))]
            df = df.set_index('date')
            df = df.sort_index()
            print df


            s = ''
            for date in df.index:
                s = s + date.strftime(u'%Y/%m/%d') + u'：解禁' + str(df.loc[date, u'占总股本比例%']) + u'%\n'
            print s
            output = output.append({
                u'股票代码':stock_list.index[i],
                u'解禁期':s
            },
            ignore_index=True)
            output.to_excel(u'C:\\Users\\Administrator\\Desktop\\stock_解禁.xlsx')

        except:
            print traceback.format_exc()


    for i in range(stock_list.shape[0]):
        try:
            stock_code = stock_list['stock_type'].iloc[i] + stock_list.index[i]
            print 'stock:', stock_code

            resp = requests_manager.get_html('http://emweb.securities.eastmoney.com/PC_HSF10/ProfitForecast/ProfitForecastAjax?code=%s' %stock_code)
            data_l = json.loads(resp)['Result']['pjtj']
            # data_l = pd.read_json(data)
            res = pd.DataFrame([])
            for d in data_l:
                # print d
                d['stock_code'] = stock_list.index[i]
                res = res.append(d,ignore_index=True)
            output = output.append({
                u'股票代号':stock_list.index[i],
                u'3月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'3月内']['mr'].iloc[0], res[res['sjd'] == u'3月内']['zc'].iloc[0]),
                u'6月内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'6月内']['mr'].iloc[0], res[res['sjd'] == u'6月内']['zc'].iloc[0]),
                u'1年内机构评级统计': u"买入：%s，增持：%s。" % (res[res['sjd'] == u'1年内']['mr'].iloc[0], res[res['sjd'] == u'1年内']['zc'].iloc[0])
            },
            ignore_index=True)
            print output
            output.to_excel('C:\Users\Administrator\Desktop\stock_predict.xlsx')
        except:
            print traceback.format_exc()

    # 东方财富网研报
    # with open('url.txt', 'r') as f:
    #     s = f.read().strip()

    # s = requests_manager.get_html('http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=HYSR&mkt=0&stat=0&cmd=4&code=&sc=&ps=5000&p=1&rt=50535713')
    # with open('url.txt', 'w') as f:
    #     f.write(s)
    #
    # # 个股研报
    # ori_data = json.loads(s[1:-1])
    # ori_data = pd.DataFrame([s.split(',') for s in ori_data]).dropna()
    # # print ori_data
    # ori_data[1] = pd.to_datetime(ori_data[1]).copy()
    # ori_data = ori_data[ori_data[1] >= datetime.datetime(year=2017, month=12, day=1)]
    # print ori_data.shape#.head(10)
    # ori_data = ori_data[ori_data[10].isin([u"房地产",u"钢铁行业",u"机械行业",u"煤炭采选",u"石油行业", u"化工行业", u"水泥建材", u"有色金属", u"造纸印刷"])]
    # print ori_data.shape#.head(10)

    # file_name = u"股票研报.txt"

    # for i in range(ori_data.shape[0]):
    #     try:
    #         url = 'http://data.eastmoney.com/report/%s/%s.html' %(ori_data['datetime'].iloc[i].strftime('%Y%m%d'), ori_data['infoCode'].iloc[i])
    #         resp = requests_manager.get_html(url)
    #         print url
    #         bs_obj = bs4.BeautifulSoup(resp,'html.parser')
    #         title = bs_obj.find('div', class_='report-title').get_text(strip=True)
    #         organization = ori_data['insName'].iloc[i]
    #
    #         s = re.search(r'(?<=<div class="newsContent">).+?(?=</div>)', resp, re.S).group()
    #         str_list = re.findall(r'(?<=<p>).+?(?=</p>)', s)
    #         with open(file_name, 'a') as f:
    #             # f.write("%s %s：%s\n" %(ori_data['datetime'].iloc[i].strftime(u'%Y%m%d'), organization, title))
    #             f.write("%s%s：%s\n" % (organization, ori_data['datetime'].iloc[i].strftime(u'%m月%d日'), title))
    #             for s in str_list:
    #                 f.write(s.replace(r'</p><p>', '\n'))
    #             f.write("\n\n")
    #
    #     except:
    #         print traceback.format_exc()

    # for i in range(ori_data.shape[0]):
    #     try:
    #         url = 'http://data.eastmoney.com/report/%s/hy,%s.html' %(ori_data[1].iloc[i].strftime('%Y%m%d'), ori_data[2].iloc[i])
    #         resp = requests_manager.get_html(url)
    #         print url
    #         bs_obj = bs4.BeautifulSoup(resp,'html.parser')
    #         title = bs_obj.find('div', class_='report-title').get_text(strip=True)
    #         organization = ori_data[4].iloc[i]
    #
    #         s = re.search(r'(?<=<div class="newsContent">).+?(?=</div>)', resp, re.S).group()
    #         str_list = re.findall(r'(?<=<p>).+?(?=</p>)', s)
    #         file_name = ori_data[10].iloc[i] + '.txt'
    #         with open(file_name, 'a') as f:
    #             # f.write("%s %s：%s\n" %(ori_data['datetime'].iloc[i].strftime(u'%Y%m%d'), organization, title))
    #             f.write("%s%s：%s\n" % (organization, ori_data[1].iloc[i].strftime(u'%m月%d日'), title))
    #             for s in str_list:
    #                 f.write(s.replace(r'</p><p>', '\n'))
    #             f.write("\n\n\n")
    #
    #     except:
    #         print traceback.format_exc()



    # ##行业研报
    # l = [s0.split(',') for s0 in s.split('","')]
    # ori_data = pd.DataFrame(l).dropna()
    # ori_data[1] = pd.to_datetime(ori_data[1]).copy()
    # print ori_data
    # file_name = u"有色金属.txt"
    #
    # for i in range(ori_data.shape[0]):
    #     try:
    #         url = 'http://data.eastmoney.com/report/%s/hy,%s.html' %(ori_data[1].iloc[i].strftime('%Y%m%d'), ori_data[2].iloc[i])
    #         resp = requests_manager.get_html(url)
    #         # with open('test.html','w') as f:
    #         #     f.write(resp)
    #         print url
    #         bs_obj = bs4.BeautifulSoup(resp,'html.parser')
    #         # e_div = bs_obj.find('div', class_='newsContent')
    #         title = bs_obj.find('div', class_='report-title').get_text(strip=True)
    #         organization = ori_data[4].iloc[i]
    #         #
    #         # with open(file_name, 'a') as f:
    #         #     f.write("%s %s：%s" %(title, organization, ori_data[1].iloc[i].strftime(u'%Y%m%d')))
    #         #     f.write(e_div.get_text())
    #         #     f.write('')
    #         # time.sleep(1)
    #
    #         s = re.search(r'(?<=<div class="newsContent">).+?(?=</div>)', resp, re.S).group()
    #         str_list = re.findall(r'(?<=<p>).+?(?=</p>)', s)
    #         with open(file_name, 'a') as f:
    #             f.write("%s %s：%s\n" %(ori_data[1].iloc[i].strftime(u'%Y%m%d'), organization, title))
    #             for s in str_list:
    #                 f.write('' + s.replace(r'</p><p>', '\n'))
    #             f.write("\n\n")
    #
    #     except:
    #         print traceback.format_exc()






# http://dc.simuwang.com/ranking/get?page=1&condition=fund_type%3A1%2C6%2C4%2C3%2C8%2C2%3Bret%3A1%3Brating_year%3A1%3Bstrategy%3A1%3Bistiered%3A0%3Bcompany_type%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A
# http://dc.simuwang.com/ranking/get?page=1&condition=fund_type%3A7%3Bret%3A1%3Brating_year%3A1%3Bstrategy%3A1%3Bistiered%3A0%3Bcompany_type%3A1%3Bsort_name%3Aprofit_col2%3Bsort_asc%3Adesc%3Bkeyword%3A
