# -*- coding:utf-8 -*-  
"""
--------------------------------
    @Author: Dyson
    @Contact: Weaver1990@163.com
    @file: driver_manager.py
    @time: 2017/10/30 15:56
--------------------------------
"""
import copy
import sys
import os
import traceback

import selenium.webdriver
import bs4
import random
#import pyvirtualdisplay
import time
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

sys.path.append(sys.prefix + "\\Lib\\MyWheels")
reload(sys)
sys.setdefaultencoding('utf8')
import requests



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


class driver_manager(object):
    def __init__(self):
        pass

    def initialization(self, engine='PhantomJS', time_out=180, **kwargs):
        driver = getattr(self, engine)
        driver = driver(**kwargs)
        driver.set_page_load_timeout(time_out)
        return driver

    def get_header(self):
        return self.headers

    def Chrome(self, **kwargs):
        # 不让Chrome显示界面
        #display = pyvirtualdisplay.Display(visible=False)
        #display.start()

        options = selenium.webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        driver = selenium.webdriver.Chrome(chrome_options=options)

        #display.stop()
        driver.set_window_size(100, 100)
        return driver

    def PhantomJS(self, **kwargs):
        """
        service_args = {
            '--load-images':'no',
            '--disk-cache':'yes',
            '--ignore-ssl-errors':'true'
        }
        """
        # 设置header
        self.user_agent = random.choice(user_agent_list)
        self.headers = {'Accept': '*/*',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Cache-Control': 'max-age=0',
                       'User-Agent': self.user_agent,#'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
                       'Connection': 'keep-alive'
                       }
        print "self.user_agent: ",self.user_agent

        desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

        for key, value in self.headers.iteritems():
            desired_capabilities['phantomjs.page.customHeaders.{}'.format(key)] = value
        desired_capabilities['phantomjs.page.customHeaders.User-Agent'] = self.user_agent#'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'

        # 优化设置
        service_args = {
            'load_images':'no',
            'disk_cache':'yes',
            'ignore_ssl_errors':'true'
        }

        #print service_args
        service_args.update(kwargs)
        #print service_args
        service_args = ['--%s=%s' %(key.replace('_','-'), service_args[key]) for key in service_args]

        #print service_args
        driver = selenium.webdriver.PhantomJS(desired_capabilities=desired_capabilities, service_args=service_args)
        return driver

    def get_html(self, url, engine='PhantomJS'):
        driver = self.initialization(engine=engine)
        driver.get('about:blank')
        driver.get(url)

        html = driver.page_source
        driver.quit()
        return html


if __name__ == '__main__':
    driver_manager = driver_manager()
    url = "http://www.simuwang.com/"
    #s = driver_manager.get_html('http://fund.eastmoney.com/fund.html#os_0;isall_0;ft_;pt_1')
    driver = driver_manager.initialization()
    driver.get(url)
    # domain = ".simuwang.com"
    # path = "/"
    cookie0 = {"cur_ck_time":"1514945128;",
        "ck_request_key":"O5K2PsIhrWt%2F6oeM707he2IVJiVJHlIQsuVY4FJYNy0%3D;",
        "http_tK_cache":"ace8a7139a833b6878b32b4c2479b7ad828fb7c1;",
        "passport":"55635%09user_13575486859%09VFJRD1BWBQ9eUFgHBFdUUFdVCwFQBwZUCVVSVlFXUgo%3D9b207ecd5c;",
        "rz_u_p":"d41d8cd98f00b204e9800998ecf8427e%3Duser_13575486859;",
        "rz_rem_u_p":"aiFB3odpeWZHIeDOt%2FJ%2BaNkn%2F8V390t5nnkC3N3%2FbHM%3D%24KzJx4oUsxjHHhuNbZ9EmS5OMgDiO8JGftPoh1SVUL24%3D;"
    }
    # cookie0 = dict([s0.split('=') for s0 in s.split('\n')])
    # print cookie0
    # cookies = []
    for key in cookie0:
        d = {}
        d['domain'] = ".simuwang.com"
        d['path'] = "/"
        d['name'] = key.strip()
        d['value'] = cookie0[key]
        driver.add_cookie(d)

    driver.get(url)
    driver.save_screenshot('screenshot.png')

    # driver = driver_manager.initialization(engine='Chrome')  #()#

    # driver.get('http://www.simuwang.com/')
    #
    # with open('test.html','w') as f:
    #     f.write(driver.page_source)
    #
    # while not driver.find_elements_by_id('gr-login-box'):
    #     time.sleep(1)
    #     driver.find_element_by_class_name('topRight').find_element_by_tag_name('a').click()
    #     # driver.save_screenshot('screenshot.png')
    #
    # driver.save_screenshot('screenshot.png')
    # login_box = driver.find_element_by_id('gr-login-box')
    # login_box.find_elements_by_tag_name('input')[0].send_keys('13575486859')
    # login_box.find_elements_by_tag_name('input')[0].send_keys(Keys.TAB)
    # login_box.find_elements_by_tag_name('input')[2].send_keys('137982')
    # # passwd_input.click()
    # # passwd_input.send_keys('137482')
    #
    # login_buttom = login_box.find_element_by_class_name('gr-big-btn')
    # login_buttom.click()
    # print driver.get_cookies()
    #

    # import pandas as pd
    # import numpy as np
    #
    #
    # df = pd.read_csv('C:\Users\Administrator\Desktop\stock_peg.csv', dtype=np.str)
    # df = df.set_index("stock_code")
    #
    # for i in range(df.shape[0]):
    #



    #
    # for i in range(df.shape[0]):
    #     try:
    #
    #         driver = driver_manager.initialization(engine='Chrome')
    #         stock_code = df.index[i]
    #         print 'stock:', stock_code
    #
    #         driver.get('http://www.iwencai.com/stockpick/search?typed=1&preParams=&ts=1&f=1&qs=result_rewrite&selfsectsn=&querytype=&searchfilter=&tid=stockpick&w=%s+PEG' %stock_code)
    #         # with open('test.csv', 'w') as f:
    #         #     f.write(driver.page_source)
    #
    #         bs_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    #         e_table = bs_obj.find('table', class_='upright_table')
    #         e_tds = e_table.find_all('td')
    #         df.loc[stock_code, u'peg'] = e_tds[0].get_text(strip=True)
    #         df.loc[stock_code, u'预测peg'] = e_tds[1].get_text(strip=True)
    #         df.loc[stock_code, u'市盈率(pe)'] = e_tds[2].get_text(strip=True)
    #         df.loc[stock_code, u'净利润同比增长率(%)'] = e_tds[3].get_text(strip=True)
    #
    #         # print df
    #         df.to_excel('C:\Users\Administrator\Desktop\stock_data.xlsx')
    #     except:
    #         print traceback.format_exc()
    #     finally:
    #         driver.quit()

    """
    from selenium import webdriver # 引入配置对象DesiredCapabilities from selenium.webdriver.common.desired_capabilities import DesiredCapabilities dcap = dict(DesiredCapabilities.PHANTOMJS) #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器 dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS)) # 不载入图片，爬页面速度会快很多 dcap["phantomjs.page.settings.loadImages"] = False # 设置代理 service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5'] #打开带配置信息的phantomJS浏览器 driver = webdriver.PhantomJS(phantomjs_driver_path, desired_capabilities=dcap,service_args=service_args) # 隐式等待5秒，可以自己调节 driver.implicitly_wait(5) # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项 # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。 driver.set_page_load_timeout(10) # 设置10秒脚本超时时间 driver.set_script_timeout(10)
    """