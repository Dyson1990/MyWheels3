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

import random




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
        # 初始化一个网页浏览器，根据传入的参数选择使用哪个浏览器，目前支持chrome和PhantomJS
        
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
        print("self.user_agent: ",self.user_agent)

        desired_capabilities = selenium.webdriver.DesiredCapabilities.PHANTOMJS.copy()

        for key, value in self.headers.items():
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
    """
    from selenium import webdriver # 引入配置对象DesiredCapabilities from selenium.webdriver.common.desired_capabilities import DesiredCapabilities dcap = dict(DesiredCapabilities.PHANTOMJS) #从USER_AGENTS列表中随机选一个浏览器头，伪装浏览器 dcap["phantomjs.page.settings.userAgent"] = (random.choice(USER_AGENTS)) # 不载入图片，爬页面速度会快很多 dcap["phantomjs.page.settings.loadImages"] = False # 设置代理 service_args = ['--proxy=127.0.0.1:9999','--proxy-type=socks5'] #打开带配置信息的phantomJS浏览器 driver = webdriver.PhantomJS(phantomjs_driver_path, desired_capabilities=dcap,service_args=service_args) # 隐式等待5秒，可以自己调节 driver.implicitly_wait(5) # 设置10秒页面超时返回，类似于requests.get()的timeout选项，driver.get()没有timeout选项 # 以前遇到过driver.get(url)一直不返回，但也不报错的问题，这时程序会卡住，设置超时选项能解决这个问题。 driver.set_page_load_timeout(10) # 设置10秒脚本超时时间 driver.set_script_timeout(10)
    """
